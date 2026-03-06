#!/bin/bash

# go to project directory
cd /home/file/path/novatrack

# activate virtual environment
source /home/file/path/novatrack/nova/bin/activate

# run ingestion
python python_files/ingest.py

# load data to postgres
python python_files/load.py

# run dbt models
cd novatrack_dbt
dbt debug
dbt run