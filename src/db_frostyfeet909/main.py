from os import environ
import sqlalchemy
from sqlalchemy.engine import Engine
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import *
from sqlalchemy.sql.functions import *
from sqlalchemy_utils import functions as sqlalchemy_utils


class Connection:
    _engine: Engine = None

    @classmethod
    def execute_query(cls, query: str, params: dict | list[dict] = None) -> None:
        """Execute query with params, no result"""
        return cls._execute(query, params)

    @classmethod
    def execute_query_result(cls, query: str, params: dict | list[dict] = None, return_list: bool = True) -> list[dict] | dict[list]:
        """Execute query with params, with result"""
        result = cls._execute(query, params, _result=True)
        keys = list(result.keys())
        values = result.all()

        if return_list:
            return [{keys[i]: value[i] for i in range(len(keys))} for value in values]
        else:
            return {keys[i]: [value[i] for value in values] for i in range(len(keys))}

    @classmethod
    def execute_query_result_single(cls, query: str, params: dict | list[dict] = None) -> dict:
        """Execute query with params, with single result"""
        result = cls._execute(query, params, _result=True)
        keys = list(result.keys())
        values = result.fetchone()

        if not values or result.fetchone():
            raise ValueError("Incorrect number of rows returned")

        result.close()
        return {keys[i]: values[0] for i in range(len(keys))}

    @classmethod
    def _execute(cls, query: str, params: dict | list[dict] = None, _result: bool = False) -> None | CursorResult:
        """Execute query with params, Privately"""
        with cls._engine.connect() as connection:
            cur = connection.execute(sqlalchemy.text(query), params)

            if _result:
                return cur
            else:
                cur.close()

    @classmethod
    def create_database(cls):
        """Create database if not exists"""
        if not sqlalchemy_utils.database_exists(cls._engine.url):
            sqlalchemy_utils.create_database(cls._engine.url)

    @classmethod
    def drop_database(cls):
        """Drop database if not exists"""
        if sqlalchemy_utils.database_exists(cls._engine.url):
            sqlalchemy_utils.drop_database(cls._engine.url)

    @classmethod
    def verify(cls):
        """Check connection works"""
        if not cls._engine:
            raise ValueError("The engine is not defined")

        with cls._engine.connect() as con:
            pass


if __name__ == "__main__":
    pass
else:
    if not environ.get("DB_CONN"):
        raise ValueError("DB_CONN not set")

    if Connection._engine:
        raise ValueError("The engine is already defined")

    Connection._engine = sqlalchemy.create_engine(environ.get("DB_CONN"), poolclass=QueuePool)
    Connection()  # Check creates
