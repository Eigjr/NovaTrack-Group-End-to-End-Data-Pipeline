#!/bin/bash

# go to project directory
cd /home/ema-i/Desktop/novatrack

# activate virtual environment
source /home/ema-i/Desktop/novatrack/nova/bin/activate

# run ingestion
python python_files/ingest.py

# load data to postgres
python python_files/load.py

# run dbt models
cd novatrack_dbt
dbt debug
dbt run