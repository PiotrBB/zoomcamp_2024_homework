# zoomcamp_2024_homework: Week 3

## Prep
1. Create virtual env\
`python -m venv week3_venv && source week3_venv/bin/activate`\
`pip install -r requirements.txt`
2. Download files from https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page using `download_green_taxi_data.py`
3. Send files to GCS
```
gcloud auth login
gsutil mb gs://week3_green_taxi_data
gsutil cp ./data/*.parquet gs://week3_green_taxi_data
```
4. Create external table in BigQuery
```
CREATE EXTERNAL TABLE IF NOT EXISTS zoomcamp2024-412915.week3.green_taxi_data_external
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://week3_green_taxi_data/*.parquet']
)
```

5. Create BQ table
```
CREATE TABLE IF NOT EXISTS zoomcamp2024-412915.week3.green_taxi_data
AS 
SELECT * FROM zoomcamp2024-412915.week3.green_taxi_data_external
```

## Questions
### Question 1
```
SELECT count(*) FROM `zoomcamp2024-412915.week3.green_taxi_data`
```
### Question 2
```
SELECT count(distinct PULocationID) FROM `zoomcamp2024-412915.week3.green_taxi_data_external`;
SELECT count(distinct PULocationID) FROM `zoomcamp2024-412915.week3.green_taxi_data`
```
### Question 3
```
SELECT count(*) FROM `zoomcamp2024-412915.week3.green_taxi_data` where fare_amount = 0;
```
### Question 4
```
CREATE TABLE IF NOT EXISTS week3.green_taxi_data_partitioned_and_clustered
PARTITION BY DATE(lpep_pickup_datetime)
CLUSTER BY PUlocationID
AS 
SELECT * FROM week3.green_taxi_data
```
### Question 5
```
SELECT DISTINCT PULocationID FROM `week3.green_taxi_data` WHERE TIMESTAMP_TRUNC(lpep_pickup_datetime, DAY) BETWEEN TIMESTAMP("2022-06-01") AND TIMESTAMP("2022-06-30");
SELECT DISTINCT PULocationID FROM `week3.green_taxi_data_partitioned_and_clustered` WHERE TIMESTAMP_TRUNC(lpep_pickup_datetime, DAY) BETWEEN TIMESTAMP("2022-06-01") AND TIMESTAMP("2022-06-30")
```