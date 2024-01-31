# zoomcamp_2024_homework: Week 1

## Prep
1. Create pg-database and pg-admin instances\
`docker compose up`

2. Build docker image with pipeline
`docker build -t pipeline:0.1 .`

3. Run docker image with args
```
docker run \
--network=week1_default \
pipeline:0.1 \
--host=pg-database \
--port=5432 \
--database=ny_taxi \
--user=root \
--password=pwd \
--taxi_table=green_taxi_trips \
--zones_table=zones \
--csv_file_download_link=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz \
--csv_file=green_tripdata_2019-09.csv.gz \
--zone_file_download_link=https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv \
--zone_file=taxi+_zone_lookup.csv
```

## Questions
### Question 3
```
SELECT
count(1)
FROM 
green_taxi_trips
WHERE 
TO_TIMESTAMP(lpep_pickup_datetime, 'YYYY-MM-DD HH24:MI:SS') >= TO_TIMESTAMP('2019-09-18 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
AND TO_TIMESTAMP(lpep_dropoff_datetime, 'YYYY-MM-DD HH24:MI:SS') <= TO_TIMESTAMP('2019-09-18 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
```

### Question 4
```
WITH max_trip AS (
SELECT
MAX(trip_distance) AS max_distance
FROM
green_taxi_trips),
dataset AS (
SELECT
trip_distance AS distance
, LEFT(lpep_pickup_datetime, 10) AS pickup_date
FROM
green_taxi_trips)
SELECT pickup_date FROM dataset JOIN max_trip ON dataset.distance = max_trip.max_distance
```

### Question 5
```
WITH dataset AS (
SELECT
t."PULocationID"
, t.total_amount
, z."Borough"
FROM
green_taxi_trips t JOIN zones z ON t."PULocationID" = z."LocationID"
WHERE
LEFT(t.lpep_pickup_datetime, 10) = '2019-09-18'
AND z."Borough" != 'Unknown'),
aggs AS (
SELECT
"Borough" as borough
, SUM(total_amount) as total
FROM
dataset
GROUP BY
"Borough")
SELECT
*
FROM
aggs
WHERE
total > 50000
ORDER BY 1 ASC
```

### Question 6
```
WITH pickup AS (
SELECT
t."PULocationID"
, t.tip_amount
, z."Zone"
FROM
green_taxi_trips t JOIN zones z ON t."PULocationID" = z."LocationID"
WHERE
LEFT(t.lpep_pickup_datetime, 7) = '2019-09'
AND z."Zone" = 'Astoria'),
max_tip AS (
SELECT
MAX(tip_amount) AS max_tip
FROM
pickup)
SELECT
z."Zone"
FROM
green_taxi_trips t JOIN zones z ON t."DOLocationID" = z."LocationID"
JOIN max_tip mt ON t.tip_amount = mt.max_tip
```

### Question 7
```

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the
following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.zoomcamp2024-dataset will be created
  + resource "google_bigquery_dataset" "zoomcamp2024-dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "demo_dataset_zoomcamp2024"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = true
      + effective_labels           = (known after apply)
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "EU"
      + max_time_travel_hours      = (known after apply)
      + project                    = "zoomcamp2024-412915"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = (known after apply)
    }

  # google_storage_bucket.zoomcamp2024-bucket will be created
  + resource "google_storage_bucket" "zoomcamp2024-bucket" {
      + effective_labels            = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "EU"
      + name                        = "demo_bucket_zoomcamp2024"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + rpo                         = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = (known after apply)
      + uniform_bucket_level_access = (known after apply)
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "Delete"
            }
          + condition {
              + age                   = 365
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }
      + lifecycle_rule {
          + action {
              + type = "AbortIncompleteMultipartUpload"
            }
          + condition {
              + age                   = 10
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value:
  ```