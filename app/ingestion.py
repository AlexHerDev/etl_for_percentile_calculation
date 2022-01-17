from typing import List

import pandas as pd
import psycopg2
from icecream import ic
from sqlalchemy import create_engine

from app.constants import *
from app.utils import remove_tables_if_more_than_three


def get_list_of_columns_yellow_taxi_trip_records() -> List[str]:
    return ["VendorID",
            "tpep_pickup_datetime",
            "tpep_dropoff_datetime",
            "passenger_count", 
            "trip_distance",
            "pickup_longitude", 
            "pickup_latitude", 
            "RatecodeID",
            "store_and_fwd_flag",
            "dropoff_longitude",
            "dropoff_latitude",
            "PULocationID",
            "DOLocationID",
            "payment_type",
            "fare_amount",
            "extra",
            "mta_tax",
            "tip_amount",
            "tolls_amount",
            "improvement_surcharge",
            "total_amount",
            "congestion_surcharge"]

def create_table(table_name: str) -> None: 
    SQL: str = f"""CREATE TABLE {table_name} ( 
        \"VendorID\" INT, 
        tpep_pickup_datetime CHAR(20), 
        tpep_dropoff_datetime CHAR(20), 
        passenger_count INT, 
        trip_distance FLOAT, 
        pickup_longitude CHAR(25) DEFAULT NULL, 
        pickup_latitude CHAR(25) DEFAULT NULL, 
        \"RatecodeID\" INT, 
        store_and_fwd_flag CHAR(1), 
        dropoff_longitude CHAR(25) DEFAULT NULL, 
        dropoff_latitude CHAR(25) DEFAULT NULL, 
        \"PULocationID\" INT DEFAULT NULL, 
        \"DOLocationID\" INT DEFAULT NULL, 
        payment_type INT, 
        fare_amount MONEY, 
        extra MONEY, 
        mta_tax MONEY, 
        tip_amount MONEY, 
        tolls_amount MONEY, 
        improvement_surcharge MONEY, 
        total_amount MONEY, 
        congestion_surcharge MONEY DEFAULT NULL)"""
  
    SQL_DROP_TABLE: str = f"DROP TABLE IF EXISTS {table_name}" 
    
    remove_tables_if_more_than_three()
    
    conn = psycopg2.connect(DSN)
    print(f"Creating table {table_name}")
    
    with conn:
        with conn.cursor() as curs:
            curs.execute(SQL_DROP_TABLE)
            curs.execute(SQL)
    conn.close()
    print(f"Table {table_name} is created")

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    #Remove NaN, Na, values
    df['trip_distance'] = df['trip_distance'].fillna(-1)
    df['VendorID'] = df['VendorID'].fillna(0).astype(int)
    df['passenger_count'] = df['passenger_count'].fillna(0).astype(int)
    df['RatecodeID'] = df['RatecodeID'].fillna(0).astype(int)
    df['payment_type'] = df['payment_type'].fillna(0).astype(int)
    
    #If you want to remove rows with negative values in trip_distance field
    #return df[df.trip_distance > 0]
    
    return df 
     
def csv_to_pgsql_db(url: str, table_name: str, chunk_size: int) -> None: 
    engine = create_engine(DSN)
    print(f"Storing data in {table_name}")
    
    for df in pd.read_csv(url, 
                          engine='c', 
                          chunksize=chunk_size, 
                          #skiprows=1, 
                          dtype={'trip_distance':float},
                          low_memory=False):
        
        df = clean_data(df)
        
        df.to_sql(
            table_name, 
            engine,
            index=False,
            if_exists='append' # if the table already exists, append this data
        )
