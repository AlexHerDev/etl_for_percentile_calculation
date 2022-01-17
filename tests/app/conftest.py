import pandas as pd 
from typing import Dict, List
from unittest import mock
import os 
import pytest
from pandas._libs.missing import NA

data_remove_bad_values_trip_distance: Dict = {
    'VendorID': [1, 2, 3, 4, 5],
    'passenger_count': [1, 2, 3, 4, 5],
    'trip_distance': [0, -1, 0.0, -1.3, 4],
    'RatecodeID': [1, 2, 3, 4, 5],
    'payment_type': [1, 2, 1, 2, 5],
    'str_field': ['a', '2', '3', 'ff', 'dd']
} 

result_remove_bad_values_trip_distance: Dict = {
    'VendorID': [5],
    'passenger_count': [5],
    'trip_distance': [4.0],
    'RatecodeID': [5],
    'payment_type': [5],
    'str_field': ['dd']
} 

df_remove_bad_values_trip_distance: pd.DataFrame = pd.DataFrame(data_remove_bad_values_trip_distance)
df_result_remove_bad_values_trip_distance: pd.DataFrame = pd.DataFrame(result_remove_bad_values_trip_distance)

data_nan_to_zero: Dict = {
    'VendorID': [1, 2, NA, 4, 5],
    'passenger_count': [1, 2, 3, 4, 5],
    'trip_distance': [1, 2, 3, 4, 5],
    'RatecodeID': [1, 2, None, 4, 5],
    'payment_type': [1, 2, 1, 2, 5],
    'str_field': ['a', '0', '3', 'ff', 'dd']    
}

result_nan_to_zero: Dict = {
    'VendorID': [1, 2, 0, 4, 5],
    'passenger_count': [1, 2, 3, 4, 5],
    'trip_distance': [1, 2, 3, 4, 5],
    'RatecodeID': [1, 2, 0, 4, 5],
    'payment_type': [1, 2, 1, 2, 5],
    'str_field': ['a', '0', '3', 'ff', 'dd']
} 

df_nan_to_zero: pd.DataFrame = pd.DataFrame(data_nan_to_zero)
df_result_nan_to_zero: pd.DataFrame = pd.DataFrame(result_nan_to_zero)

url_expected = "https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2020-03.csv"

list_of_columns_yellow_taxi_trip_records: List[str] = ["VendorID",
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

SQL_CREATE_TABLE_TEST: str = "CREATE TABLE IF NOT EXISTS test (\
    key INT, \
    value_to_cal_perc FLOAT)"

SQL_FILL_TABLE_TEST: str = "INSERT INTO public.test (key, value_to_cal_perc) \
VALUES (1, 1.0), (2, 2.0), (3, 3.0), (4, 4.0), (5, 5.0), (6, 6.0), (7, 7.0), \
(8, 8.0), (9, 9.0), (10, 10.0);"    


result_expected_perc_0_90: List[List] = [[10, 10.0]]

result_expected_perc_0_40: List[List] = [[5, 5.0], 
                                         [6, 6.0], 
                                         [7, 7.0],
                                         [8, 8.0],
                                         [9, 9.0],
                                         [10, 10.0]]