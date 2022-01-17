import pytest
from tests.app.conftest import *

@mock.patch.dict(os.environ, {"POSTGRES_PORT": "5432"})
def test_to_str_params():
    month=3
    year=2020
    from app.utils import to_str_params
    assert '03', '2020' == to_str_params(month, year) 

@mock.patch.dict(os.environ, {"POSTGRES_PORT": "5432"})    
def test_get_file_url() -> str:
    month=3
    year=2020
    from app.utils import get_file_url
    assert url_expected == get_file_url(month, year) 
    
@mock.patch.dict(os.environ, {"POSTGRES_PORT": "5432"})    
def test_get_table_name() -> str:
    month=3
    year=2020
    from app.utils import get_table_name
    assert "table_yttr_2020_03" == get_table_name(month, year)   