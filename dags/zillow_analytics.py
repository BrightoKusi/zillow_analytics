from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
import pandas as pd
import boto3
import json 
import requests 

access_key_id = Variable.get("aws_access_key_id")
secret_access_key = Variable.get("aws_secret_access_key")

transformed_csv_data_bucket = 'zillow-transformed-data-bok'


with open('/opt/airflow/dags/config_api.json', 'r') as config_file:
    api_host_key = json.load(config_file)

querystring = {"location":"houston, tx","output":"json","status":"forSale","sortSelection":"priorityscore","listing_type":"by_agent","doz":"any"}

dt_now_string = datetime.now().strftime('%d%M%Y%H%M%S')

def extract_zillow_data(**kwargs):
    url = kwargs['url']
    headers = kwargs['headers']
    querystring = kwargs['params']
    dt_string = kwargs['date_string']



    response = requests.get(url, headers=headers, params=querystring)

    zillow_data = response.json()

    
    bucket_name = 'zillow-raw-data-bok'
    object_key = f'zillow_data_{dt_string}.json'    

    #specify the output filepath 
    output_file_path = fr"s3://zillow-raw-data-bok/zillow_data_{dt_string}.json"
    file_str = f"zillow_data_{dt_string}.csv"

    output_list = [output_file_path, file_str]
        
    s3_client = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=json.dumps(zillow_data).encode('utf-8'))

    return output_list


default_args = {
    'owner': 'bright',
    'start_date': datetime(2024, 9, 23)
}

with DAG('zillow_analytics_dag',
         default_args=default_args,
         schedule_interval='@weekly',
         catchup=False) as dag:
    
    extract_zillow_data_to_s3 = PythonOperator(
        task_id = "tsk_extract_zillow_data_to_s3"
        , python_callable = extract_zillow_data
        , op_kwargs = {'url': 'https://zillow56.p.rapidapi.com/search', 'headers': api_host_key,  'params': querystring, 'date_string':dt_now_string}
    )

    poking_for_transformed_csv_file = S3KeySensor(
        task_id='tsk_poking_for_transformed_csv_file',
        bucket_key="{{ ti.xcom_pull(task_ids='tsk_extract_zillow_data_to_s3')[1] }}",  # Use correct task_id reference
        bucket_name=transformed_csv_data_bucket,
        aws_conn_id='aws_s3_conn',
        wildcard_match=False,
        timeout=120,
        poke_interval=5
    )

    transfer_data_from_s3_to_redshift = S3ToRedshiftOperator(
        task_id = 'tsk_transfer_data_from_s3_to_redshift'
        , aws_conn_id = 'aws_s3_conn'
        , redshift_conn_id = 'conn_id_redshift'
        , s3_bucket = transformed_csv_data_bucket
        , s3_key = "{{ ti.xcom_pull(task_ids='tsk_extract_zillow_data_to_s3')[1] }}"
        , schema = 'PUBLIC'
        , table = 'zillow_data'
        , copy_options = ["csv IGNOREHEADER 1"]
    )

    extract_zillow_data_to_s3 >> poking_for_transformed_csv_file >> transfer_data_from_s3_to_redshift