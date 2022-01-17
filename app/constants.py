import os 

DOMAIN: str = "https://s3.amazonaws.com"
ENDPOINT: str = "/nyc-tlc/trip+data/"
BASE_FILE_NAME: str = "yellow_tripdata_"
FILE_EXTENSION: str = ".csv"

POSTGRES_USER: str = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT"))
POSTGRES_DB: str = os.getenv("POSTGRES_DB")
POSTGRES_ADDRESS: str = os.getenv("POSTGRES_ADDRESS")
TABLE_BASE_NAME: str = "table_yttr"
TABLE_RESULT_PERFORMANCE_NAME: str = "table_performance"

MAX_TABLES_IN_DB: int = 3

DSN: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db/{POSTGRES_DB}"

DSN_TEST: str = f"test_db"
