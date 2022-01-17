import time
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from icecream import ic

from app.constants import *
from app.ingestion import create_table, csv_to_pgsql_db
from app.percentile_calculation import get_percentile
from app.utils import *

app = FastAPI()


@app.get("/", tags=["Home"])
def read_root():
    return {"message": "API FOR PERCENTILE CALCULATION"}

@app.post("/store_data/{month}/{year}", tags=["Ingestion"])
def store_data(month: int, year: int):
    table_name: str = get_table_name(month, year)    
    data_url: str = get_file_url(month, year)
    elapsed: float = 0.0

    if not check_if_table_exist(table_name):
        start = time.perf_counter()
        create_table(table_name)
        csv_to_pgsql_db(url=data_url, table_name=table_name, chunk_size=10000)
        elapsed = round(time.perf_counter() - start, 4)

        data_performance = create_dict_table_performance('ingestion_process',
                                                        f"{elapsed}",
                                                        month,
                                                        year) 
        insert_performance_results(data_performance)
    
    return f"Data stored in table {table_name} succesfully"

@app.get("/all_trips_in_distance_travelled_over/{month}/{year}/{percentile}/{offset}/{limit}", tags=["Percentile calculation"]) #, response_model=YellowTaxiTripsPercentile)
def calculate_percentile(month: int, year: int, percentile: float, offset: int, limit: int):
    table_name: str = get_table_name(month, year)
    
    if not check_if_table_exist(table_name):
        raise HTTPException(status_code=404, detail=f"You need to store data first for table with month {month} and year {year}")
    
    start: float = time.perf_counter()
    result = get_percentile(table_name, percentile, offset, limit)
    elapsed: float = round(time.perf_counter() - start, 4)

    data_performance = create_dict_table_performance(f'percentile_{str(percentile)}_calculation_process',
                                                    f"{elapsed}",
                                                    month,
                                                    year)
    
    insert_performance_results(data_performance)
    
    return result 

@app.get("/performance", tags=["Performance stats"])
def get_performance() -> List[Dict[str, str]]:
    if not check_if_table_exist(TABLE_RESULT_PERFORMANCE_NAME):
        raise HTTPException(status_code=404, detail=f"No executions yet")
    result: List[List] = get_performance_stats()
    result_dict: List[Dict] = []

    for data in result: 
        result_dict.append({'Task': data[0].rstrip(), 
                            'Time_execution_in_secs': data[1].rstrip(),
                            'Date execution': data[2].rstrip(),
                            'month_csv': data[3].rstrip(),
                            'year_csv': data[4].rstrip()}) 

    return result_dict
 
