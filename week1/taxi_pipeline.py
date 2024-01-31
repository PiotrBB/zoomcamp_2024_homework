import argparse
from time import time
import os

import numpy as np
import pandas as pd
from sqlalchemy import create_engine

parser = argparse.ArgumentParser(description='Ingest Taxi CSV into Postgres')

parser.add_argument('--host', help='Postgres host')
parser.add_argument('--port', help='Postgres port')
parser.add_argument('--database', help='Postgres database')
parser.add_argument('--user', help='Postgres user')
parser.add_argument('--password', help='Postgres password')
parser.add_argument('--taxi_table', help='Postgres Taxi table')
parser.add_argument('--zones_table', help='Postgres Zones table')
parser.add_argument('--csv_file_download_link', help='CSV file download link')
parser.add_argument('--csv_file', help='CSV file to ingest')
parser.add_argument('--zone_file_download_link', help='Zone file download link')
parser.add_argument('--zone_file', help='Zone file to ingest')


args = parser.parse_args()

def download_file(url, filename):
    print(f'Downloading {url} to {filename}')
    start = time()
    os.system(f'wget {url} -O {filename}')
    end = time()
    print(f'File donloaded in {end - start:.2f} seconds')
    
def read_file(filename):
    print(f'Reading {filename}')
    start = time()
    df = pd.read_csv(filename)
    end = time()
    print(f'File read in {end - start:.2f} seconds')
    return df

def main(params):
    host = params.host
    port = params.port
    database = params.database
    user = params.user
    password = params.password
    taxi_table = params.taxi_table
    zones_table = params.zones_table
    csv_file_download_link = params.csv_file_download_link
    csv_file = params.csv_file
    zone_file_download_link = params.zone_file_download_link
    zone_file = params.zone_file

    download_file(csv_file_download_link, csv_file)
    download_file(zone_file_download_link, zone_file)
    
    df = read_file(csv_file)
    df_zones = read_file(zone_file)
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

    print('Writing zones to Postgres')   
    df_zones.to_sql(zones_table, engine, if_exists='replace', index=False)
    print('Zones written to Postgres')
    
    print('Writing data to Postgres')   
    df.head(0).to_sql(taxi_table, engine, if_exists='replace', index=False)
    dfs = np.array_split(df, 10)
    for df in dfs:
        start = time()
        df.to_sql(taxi_table, engine, if_exists='append', index=False)
        end = time()
        print(f'Chunk written to Postgres in {end - start:.2f} seconds')

if __name__ == '__main__':
    
    main(args)
