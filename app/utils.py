from datetime import datetime
from typing import Dict, List

import psycopg2

from app.constants import *


def to_str_params(month: int, year: int):
    month_str: str = str(month) if month >= 10 else f"0{str(month)}"
    year_str: str = str(year)
    return month_str, year_str 

def get_file_url(month: int, year: int) -> str:
    month_str, year_str = to_str_params(month, year)
    return f"{DOMAIN}{ENDPOINT}{BASE_FILE_NAME}{year_str}-{month_str}{FILE_EXTENSION}"

def get_table_name(month: int, year: int) -> str:
    month_str, year_str = to_str_params(month, year)
    return f"{TABLE_BASE_NAME}_{year_str}_{month_str}"    

def create_dict_table_performance(process_msg: str, elapsed: str, month: int, year: int) -> Dict[str, str]:
    data_performance: Dict = {}
    data_performance['proccess'] = process_msg
    data_performance['time_executing'] = elapsed   
    data_performance['execution_date'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    data_performance['month'] = str(month)
    data_performance['year'] = str(year)

    return data_performance

def check_if_table_exist(table_name: str) -> bool:
    exist: bool = False

    conn = psycopg2.connect(DSN)
    with conn:
        with conn.cursor() as curs:
            curs.execute("select exists(select * from information_schema.tables where table_name=%s)", (table_name,))
            exist = curs.fetchone()[0]
    conn.close()   
    
    return exist

def create_table_performance() -> None: 
    SQL: str = f"CREATE TABLE {TABLE_RESULT_PERFORMANCE_NAME} \
        (proccess CHAR(40), \
        time_executing CHAR(10), \
        execution_date CHAR(20), \
        month CHAR(2), \
        year CHAR(4))"
  
    if not check_if_table_exist(TABLE_RESULT_PERFORMANCE_NAME):    
        conn = psycopg2.connect(DSN)
        print(f"Creating table {TABLE_RESULT_PERFORMANCE_NAME}")
        with conn:
            with conn.cursor() as curs:
                curs.execute(SQL)
        conn.close()
    print(f"Table {TABLE_RESULT_PERFORMANCE_NAME} is created")   

def insert_performance_results(data_result: Dict) -> None:
    create_table_performance()
    SQL: str = f"INSERT INTO public.{TABLE_RESULT_PERFORMANCE_NAME} (proccess, time_executing, execution_date, month, year)  VALUES (%s, %s, %s, %s, %s);"
    data = (data_result['proccess'], 
            data_result['time_executing'], 
            data_result['execution_date'],
            data_result['month'],
            data_result['year']) 
    conn = psycopg2.connect(DSN)
    print(f"Creating table {TABLE_RESULT_PERFORMANCE_NAME}")
    with conn:
        with conn.cursor() as curs:
            curs.execute(SQL, data)
    conn.close()

def remove_tables_if_more_than_three() -> None:
    SQL_GET_LIST: str = f"select * from information_schema.tables where table_schema = 'public'"
    conn = psycopg2.connect(DSN)
    with conn:
        with conn.cursor() as curs:
            data: List[List] = None
            curs.execute(SQL_GET_LIST)
            data = curs.fetchall()
            if len(data) > MAX_TABLES_IN_DB:
                for table in data:
                    if table[2] != TABLE_RESULT_PERFORMANCE_NAME:
                        curs.execute(f"DROP TABLE public.{table[2]}")
    conn.close()

def get_performance_stats() -> List[List]:
    SQL: str = f"SELECT * FROM public.{TABLE_RESULT_PERFORMANCE_NAME}"
    conn = psycopg2.connect(DSN)
    data: List[List] = None
    with conn:
        with conn.cursor() as curs:
            curs.execute(SQL)
            data = curs.fetchall()  
    conn.close()
   
    return data