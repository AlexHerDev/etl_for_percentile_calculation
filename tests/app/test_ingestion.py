import pytest
import pandas as pd 
import numpy as np

from tests.app.conftest import *
from icecream import ic

@mock.patch.dict(os.environ, {"POSTGRES_PORT": "5432"})
@pytest.mark.parametrize(
    "df_test, df_result",
    [(df_remove_bad_values_trip_distance, df_result_remove_bad_values_trip_distance),
     (df_nan_to_zero, df_result_nan_to_zero)
    ]
)
def test_clean_data(df_test: pd.DataFrame, df_result: pd.DataFrame):
    from app.ingestion import clean_data
    assert np.array_equal(clean_data(df_test).values, df_result.values)
    
@mock.patch.dict(os.environ, {"POSTGRES_PORT": "5432"})
def test_get_list_of_columns_yellow_taxi_trip_records():
   from app.ingestion import get_list_of_columns_yellow_taxi_trip_records 
   assert get_list_of_columns_yellow_taxi_trip_records() == list_of_columns_yellow_taxi_trip_records