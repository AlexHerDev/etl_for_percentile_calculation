from typing import Dict, List

import psycopg2
from icecream import ic

from app.constants import *
from app.ingestion import create_table


def get_percentile(table_name: str, percentile: float, offset: int, limit: int) -> List[List]: 
    #SQL_SET_PARALLEL: str = f"SET max_parallel_workers_per_gather = 4;"
    SQL_CREATE_VIEW_WITH_DATA_OVER_PERCENTILE: str = f"SELECT * FROM public.{table_name} \
        WHERE trip_distance > (select tdigest_percentile(CAST(trip_distance AS DOUBLE PRECISION), 100, {percentile}) \
        FROM public.{table_name}) offset {str(offset)} limit {str(limit)}"

    conn = psycopg2.connect(DSN)
    print(f"Calculating percentile {table_name}")
    data: Dict = {}
    with conn:
        with conn.cursor() as curs:
            #curs.execute(SQL_SET_PARALLEL)
            curs.execute(SQL_CREATE_VIEW_WITH_DATA_OVER_PERCENTILE)
            data = curs.fetchall()
    conn.close()
    
    return data
