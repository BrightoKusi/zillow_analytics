-- Create the warehouse
CREATE WAREHOUSE zillow_warehouse;

-- Drop and create the database
DROP DATABASE IF EXISTS zillow_database;
CREATE DATABASE IF NOT EXISTS zillow_database;

-- Create schema for storing data
CREATE SCHEMA zillow_database.zillow_schema;

-- Create or replace the table 
CREATE OR REPLACE TABLE zillow_database.zillow_schema.zillow_table(
            bathrooms INT
            , bedrooms INT
            , city STRING
            , homeStatus STRING
            , homeType STRING
            , livingArea INT
            , price INT
            , rentZestimate INT
            , zipcode INT
);

-- Query the table
SELECT * FROM zillow_database.zillow_schema.zillow_table LIMIT 10;

-- Create file format schema and file format
CREATE SCHEMA file_format_schema;
CREATE OR REPLACE FILE FORMAT zillow_database.file_format_schema.csv_format
    type = 'CSV'
    field_delimiter = ','
    record_delimiter = '\n'
    skip_header = 1;

-- Create external stage schema and the stage
CREATE SCHEMA external_stage_schema;
CREATE OR REPLACE STAGE zillow_database.external_stage_schema.zillow_ext_stage
    url= 's3://zillow-transformed-data-bok/' 
    credentials=(aws_key_id='AKIA3***' aws_secret_key='MU7Nu***')
    FILE_FORMAT = zillow_database.file_format_schema.csv_format;

-- List files in the external stage
LIST @zillow_database.external_stage_schema.zillow_ext_stage;

-- Create schema for snowpipe
CREATE OR REPLACE SCHEMA zillow_database.snowpipe_schema;

-- Create Snowpipe
CREATE OR REPLACE PIPE zillow_database.snowpipe_schema.zillow_snowpipe
    auto_ingest = TRUE
    AS 
    COPY INTO zillow_database.zillow_schema.zillow_table
    FROM @zillow_database.external_stage_schema.zillow_ext_stage;

-- Describe the pipe
DESC PIPE zillow_database.snowpipe_schema.zillow_snowpipe;
