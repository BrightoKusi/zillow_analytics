# Zillow Real Estate Analytics

![Zillow Pipeline Diagram](images/draw.io.drawio%20(5).png)

## 🏡 Project Overview

This project demonstrates an end-to-end real estate data analytics pipeline using Zillow data. The pipeline is designed to automate data extraction, transformation, loading, and visualization using scalable cloud technologies and best practices in data engineering.

It serves both real-time and batch analytical needs by integrating with tools like Amazon Redshift, Snowflake, Power BI, and Amazon QuickSight — providing actionable insights for business analysts and stakeholders.

---

## 🔧 Tools & Technologies

- **Language & Libraries**: Python, Boto3
- **ETL & Orchestration**: AWS Lambda, Apache Airflow
- **Data Storage**: Amazon S3, Amazon Redshift, Snowflake (via Snowpipe)
- **Visualization**: Amazon QuickSight, Power BI
- **Containerization**: Docker
- **Deployment & Reproducibility**: Dockerized services with scheduled orchestration in Airflow

---

## 🔁 Workflow

1. **API Data Extraction**  
   Zillow housing data is extracted through a public API and stored in **Amazon S3**.

2. **Transformation**  
   Data is transformed using **AWS Lambda** functions triggered on upload.

3. **Loading**  
   Transformed data is loaded into **Amazon Redshift** for analytics.

4. **Snowflake Integration**  
   A **Snowpipe** is configured to load the same data into **Snowflake** for downstream teams using **Power BI**.

5. **Visualization**  
   Primary dashboards are created using **Amazon QuickSight**; Power BI is used by external consumers.

6. **Orchestration**  
   The entire pipeline is orchestrated using **Apache Airflow** with Dockerized task scheduling.

---

## 📦 Project Structure

```plaintext
zillow_analytics/
├── dags/              # Airflow DAGs for orchestration and ETL script
├── scrips/                    # Entry point for docker
├── Utils/                    # sql scripts and helper functions 
├── docker-compose.yml/     # Docker configuration file
└── README.md                  # Project documentation

To reproduce this pipeline locally or on the cloud:

Clone the repository:
git clone https://github.com/BrightoKusi/zillow_analytics.git

Build and start services:
docker-compose up --build

Configure environment variables:
AWS credentials
Redshift and Snowflake credentials
Airflow environment configs
Deploy DAGs to Airflow and trigger manually or via schedule.
