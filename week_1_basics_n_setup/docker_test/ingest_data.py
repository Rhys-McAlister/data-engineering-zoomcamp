#!/usr/bin/env python
# coding: utf-8

import os
import argparse
import pandas as pd
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    csv_name = 'output.csv'
    # download the csv
    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")


    # df1 = pd.read_csv("yellow_tripdata_2021-01.csv.gz", compression='gzip', nrows=100)
    df1_iter = pd.read_csv(csv_name, compression='gzip', iterator=True, chunksize=100000)
    df1 = next(df1_iter)



    df1.tpep_pickup_datetime = pd.to_datetime(df1.tpep_pickup_datetime)
    df1.tpep_dropoff_datetime = pd.to_datetime(df1.tpep_dropoff_datetime)

    engine.connect()


    df1.tpep_pickup_datetime = pd.to_datetime(df1.tpep_pickup_datetime)
    df1.tpep_dropoff_datetime = pd.to_datetime(df1.tpep_dropoff_datetime)

    df1.head(n=0).to_sql(name=table_name,con=engine, if_exists='replace')

    from time import time


    while True:
        t_start = time()
        df1 = next(df1_iter)
        
        df1.tpep_pickup_datetime = pd.to_datetime(df1.tpep_pickup_datetime)
        df1.tpep_dropoff_datetime = pd.to_datetime(df1.tpep_dropoff_datetime)
        df1.to_sql(name=table_name,con=engine, if_exists='append')
        t_end = time()
        print('inserted another chunk...., took %.3f second' % (t_end - t_start))
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingest CSV data to postgres")

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='db name for postgres')
    parser.add_argument('--table_name', help='table_name')
    parser.add_argument('--url', help='url for postgres')

    args = parser.parse_args()


    main(args)




