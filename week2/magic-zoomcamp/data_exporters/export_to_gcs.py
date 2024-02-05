import pyarrow as pa
import pyarrow.parquet as pq
import os
if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/zoomcamp2024-412915-019689e27369.json"
bucket_name = 'mage-zoomcamp2024'
project_id = 'zoomcamp2024-412915'
table_name = 'week2_homework/nyc_taxi_data'
root_path = f'{bucket_name}/{table_name}'

@data_exporter
def export_data_to_google_cloud_storage(data, **kwargs) -> None:
    table = pa.Table.from_pandas(data)
    gcs = pa.fs.GcsFileSystem()
    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=['lpep_pickup_date'],
        filesystem=gcs
    )
