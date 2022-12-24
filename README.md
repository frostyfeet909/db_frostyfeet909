# db_frostyfeet909
Provides methods to work with a queue pool from SQL alchemy.


## Example
```python3
import db_frostyfeet909 as db

connection = db.Connection('postgresql+psycopg2://{USERNAME}:{PASSWORD}@{IP}/{DATABASE}')
connection.create_database()

connection.execute_query("CREATE TABLE test (key INT PRIMARY KEY, value TEXT);")
connection.execute_query("INSERT INTO test (key, value) VALUES (1, 'first');")
connection.execute_query("INSERT INTO test (key, value) VALUES (2, 'second');")

first_key = {"key": 1}
first_value = connection.execute_query_result_single("SELECT value FROM test WHERE key = :key LIMIT 1;", first_key)["value"]
print("The first value is: {0}".format(first_value))
```


