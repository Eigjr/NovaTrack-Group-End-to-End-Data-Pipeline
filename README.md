# NovaTrack-Group-End-to-End-Data-Pipeline
NovaTrack Analytics NovaTrack Analytics is the data and insights division of NovaTrack Group, focused on transforming raw operational data into actionable intelligence. The organization supports internal teams and external partners with reliable datasets for reporting, forecasting, and informed decision-making.

## Project Overview
This project demonstrates a robust, end-to-end data pipeline solution that downloads raw data from a source(weather API), loads it into a PostgreSQL database, transforms it using dbt. The entire workflow is automated with a cron job for daily execution.

### Key Features
- Data Ingestion: A Python script extracts data from a weather API and loads it into a PostgreSQL database.
* Data Transformation: dbt is used to build a data warehouse, ensuring data quality and creating a clean data model.
* Containerization: The entire pipeline (ETL, dbt, and PostgreSQL) is containerized using Docker for portability and   consistency.
* Cross-Platform Automation: A dynamic bash script orchestrates the pipeline on both WSL and Git Bash environments.
* Scheduling: A host-level cron job is set up to run the pipeline daily at a scheduled time.

## Project Architecture
A logical architecture was designed to visualize the flow of data through the pipeline.

![alt text](https://github.com/Eigjr/NovaTrack-Group-End-to-End-Data-Pipeline/blob/main/document/nova_architecture%20diagram.png?raw=true)

## Getting Started

### Prerequisites
Before you begin, ensure you have the following software installed:

* Git
* dbt
* postgres
* Windows Subsystem for Linux (WSL) or Linux sustem

## Project Setup
1. Clone the repository:

``` bash
git clone <your_remote_repository_url>
cd <your-project-directory>
```

2. Set up environment variables: Create a `.env` file in the root of the project to store your database credentials.
# Example `.env` file content
``` .env
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=your_db_name
DB_PORT=5434
DB_SCHEMA=analytics
```

3. Configure dbt profiles locally: Copy your `profiles.yml` file into the novatrack_dbt directory.

```cp /mnt/c/Users/USER/.dbt/profiles.yml ./novatrack_dbt/profiles.yml```
- Make sure your local profiles.yml is configured to read from environment variables.

# novatrack_dbt/profiles.yml
```
novatrack_dbt:
outputs:
    dev:
    dbname: your_db_name
    host: "{{ env_var('DB_HOST', 'localhost') }}"
    pass: your_password
    port: 5432
    schema: analytics
    threads: 3
    type: postgres
    user: your_user
target: dev
```

# Local Pipeline Development
- ## Python ETL Scripting

The project began with a Python script for the ETL process.

Commands:
# Activate environment
python3 -m venv venv /activate venv

### Run the ETL script
```
python 
ingest.py
load.py
location.py
```

# dbt Transformation

## After the data was loaded, dbt was used for transformation.

### Commands:

```
dbt
Navigate to the dbt project folder
cd novatravk_dbt

Debug the dbt connection
dbt debug

Run and test the models
dbt build
```

# Automating the Pipeline Locally

A bash script was created to automate the ETL and dbt process. It dynamically handles execution based on the environment (WSL or Git Bash) and logs all output to a file.
Scheduling with Cron

The bash script was scheduled to run daily at 12:00 AM using cron.

### Commands:

```
# Open the crontab for editing
crontab -e

# Add the schedule entry
0 0 * * * /path/to/your/project/run_etl_pipeline.sh 

# Check the cron service status
sudo service cron status
```

```
├── .env
├── .gitignore
├── README.md
├── run_novatrack_pipeline.sh
├── cron_daily_run.sh
├── requirements.txt
├── python_files/
│   ├──ingest.py
│   ├──load.py
│   ├──location.py
│ 
├── novatract_dbt/
│   ├── dbt_project.yml
│   ├── profiles.yml
│   ├── models/
└──
```

# Conclusion
This project provides a comprehensive blueprint for building a robust and automated data pipeline. dbt enforces data quality, making the process reliable and scalable.
