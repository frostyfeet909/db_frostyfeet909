from os import environ
import sqlalchemy
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.pool import QueuePool
from sqlalchemy.sql.functions import *


def execute_query(query: str, params: dict | list[dict] = None, _result: bool = False) -> None | CursorResult:
    """Execute query with params, no result"""
    with engine.connect() as connection:
        curr = connection.execute(sqlalchemy.text(query), params)

        if _result:
            return curr


def execute_query_result(query: str, params: dict | list[dict] = None, return_list: bool = True) -> list[dict] | dict[list]:
    """Execute query with params, with result"""
    result = execute_query(query, params, _result=True)
    values = result.fetchall()
    keys = list(result.keys())

    if return_list:
        return [{keys[i]: value[i] for i in range(len(keys))} for value in values]
    else:
        return {keys[i]: [value[i] for value in values] for i in range(len(keys))}


def execute_query_result_single(query: str, params: dict | list[dict] = None) -> dict:
    """Execute query with params, with single result"""
    result = execute_query(query, params, _result=True)
    values = result.fetchone()
    keys = list(result.keys())

    return {keys[i]: values[0] for i in range(len(keys))}


if __name__ == "__main__":
    pass
else:
    engine = sqlalchemy.create_engine(environ.get("DB_CONN"), poolclass=QueuePool)
