import json
import boto3
import pandas as pd

s3_client = boto3.client('s3')


def lambda_handler(event, context):
    # Extract bucket name and object key from the S3 event
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    # Define the target bucket and file name (assuming the original file has a ".json" extension)
    target_bucket = 'redfin-transformed-data-bok'
    target_file_name = object_key[:-5]  # Assuming you want to remove the last 5 characters

    print(f"Source Bucket: {source_bucket}, Object Key: {object_key}")
    
    # Wait until the object is available in the source bucket
    waiter = s3_client.get_waiter('object_exists')
    waiter.wait(Bucket=source_bucket, Key=object_key)
    
    # Get the object from the source bucket
    response = s3_client.get_object(Bucket=source_bucket, Key=object_key)
    real_estate_data = response['Body']
    real_estate_data = response['Body'].read().decode('utf-8')
    real_estate_data = json.loads(real_estate_data)
    
    real_estate_data_list = []
    
    for i in real_estate_data['results']:
        real_estate_data_list.append(i)
    
    real_estate_df = pd.DataFrame(real_estate_data_list)
    
    selected_columns = ['bathrooms', 'bedrooms', 'city', 'homeStatus',
                        'homeType', 'livingArea', 'price', 'rentZestimate', 'zipcode']
    real_estate_df = real_estate_df[selected_columns]
    print(real_estate_df)

    #convert dataframe to csv format
    real_estate_csv_data = real_estate_df.to_csv(index=False)
    
    #upload CSV to s3
    bucket_name = target_bucket
    object_key  = f"{target_file_name}.csv"
    
    s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=real_estate_csv_data)    
    
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('CSV conversion and s3 upload completed successfully')
    }
