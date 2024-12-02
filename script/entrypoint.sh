#!/bin/bash
set -e

# Install Python dependencies if requirements.txt is present
if [ -e "/opt/airflow/requirements.txt" ]; then
  pip install --upgrade pip
  pip install -r /opt/airflow/requirements.txt
fi

# Initialize the database if it's not already initialized
if [ ! -f "/opt/airflow/airflow.db" ]; then
  airflow db init && \
  airflow users create \
    --username admin \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@example.com \
    --password admin
fi

# Upgrade the database schema
airflow db migrate

# Start the Airflow webserver
exec airflow webserver
