import os

import psycopg2
import pytest
from tests.app.conftest import *

'''
def test_get_percentile():
    from app.constants import DSN_TEST
    from app.percentile_calculation import get_percentile

    #Atention: For test queries in a DB, it's better use another specific db for test.
    conn = psycopg2.connect(DSN_TEST)
    with conn:
        with conn.cursor() as curs:
            curs.execute(SQL_CREATE_TABLE_TEST)
            curs.execute(SQL_FILL_TABLE_TEST)
    conn.close()   
    
    assert result_expected_perc_0_90 == get_percentile('test', 0.90, 0, 10)
    assert result_expected_perc_0_40 == get_percentile('test', 0.40, 0, 10)

'''
