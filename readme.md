## An ETL for real-time analysis (percentile calculation) using Python, FastApi and PostgreSQL ##

Using yellow taxi trip records of NYC from this [web](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page), the system will storage the CSVs files and exposes in an API the percentile calculated.  

### How to run it? ###

You can use docker-compose: (You need to have installed before [Docker](https://docs.docker.com/engine/install/) and [Docker-compose](https://docs.docker.com/compose/install/)):
```
$docker-compose up
```
When all is up you will have 2 services: a Postgres database and a so simple API build with Python and FastApi.
You can visit the Api docs in http://0.0.0.0/docs#/ and interactively run the requests.

There are 3 endpoints availables:

![Image](images/img_1.png?raw=true)

- **Ingestion**: It needs to pass month (just integer values between 1-12) and year (just integer values between 2009-2021) as a parameter. This month and year indicate what csv you want for get percentile. This endpoint generate an url for take the yellow taxi trip records of NYC from this [web](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page) and insert into a table in Postgres. 
This is the first that you need to do, for percentile calculation. 

```
curl -X 'POST' \
  'http://0.0.0.0/store_data/{month}/{year}' \
  -H 'accept: application/json' \
  -d ''
```

![Image](images/img_2.png?raw=true)

- **Percentile_calculation**: Once the data is in db, you can get all the trips with trip distance over any percentile. You need to pass month (just integer values between 1-12), year (just integer values between 2009-2021), percentile in float format (0.90, 0.85, 0.10), and offset and limit for choose the result part that you want. (Offset=15000 and limit=5000 return 5000 rows from 15000 row in result).   

```
curl -X 'GET' \
  'http://0.0.0.0/all_trips_in_distance_travelled_over/{month}/{year}/{percentile}/{offset}/{limit}' \
  -H 'accept: application/json'
```

![Image](images/img_3.png?raw=true)

- **Performance stats**: This endpoint doesnt require params, just call it and get a very simple stats of performance in time.  

```
curl -X 'GET' \
  'http://0.0.0.0/performance' \
  -H 'accept: application/json'
```

![Image](images/img_4.png?raw=true)

### How to test it? ###
More tests will be adde soon. 

No coverage stats in the project.

### How it works? ###
In the first step begin the ingestion. Data are getting from url and store in a table for each set of data. It's means that tables will contain the data related to trips for a concrete month and year. This can be slow cause of this process will download the csv for get the data. 

In a second step, you query the tables for get the percentile and select a part of this results (you need to use limit and offset). The idea is not create a big table with all the data, if show to the user a part of this data always
and let him iterate for the result. For a future improvement, the results would be in .csv.

For calculate the percentile I used a Tdigest algorithm. I compared Tdigest with the native function for calculate 
percentile in Postgress and the difference is quite good.  

Also, I always use a profiler for try to improve performance once I have an e2e execution. In this time, I created a very simple resume of executions times (not memory stats) that you can to get in the "get_performance" endpoint. This stats are not realistics at all, but works for this approach.   

### Some considerations ###
One of the most confusing thing that happen me when build this is that there are two differents maps of fields for data
schema.
So I can't see all the csv for associate month-year to a concrete map. I solved it adding fields with null as default value. The problem with this solution is the nulls in tables when this fields dont exist, will be a lot of it. 

Other consideration is that the store memory. Large CSVs will generate big tables size in db. DB is in local, so for 
a limited memory machines (that's me) it necessary drop the tables. I use a max of 3 tables in the database. This means that ingestion endpoint just will works with a max of 2 parallel requests.

