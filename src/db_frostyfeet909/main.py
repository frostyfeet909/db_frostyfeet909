import sqlalchemy
from sqlalchemy.engine.url import URL
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.pool import QueuePool, Pool
from sqlalchemy_utils import functions as sqlalchemy_utils


class Connection:
    """A wrapper for a sqlalchemy engine.

    Provides methods for acting on implicitly created sqlalchemy engine/pool. Thread safe.
    """

    def __init__(self, url: URL, pool: Pool = None):
        self._engine = sqlalchemy.create_engine(url, poolclass=(QueuePool if not pool else pool))

    def execute_query(self, query: str, params: dict | list[dict] = None) -> None:
        """Execute query with params, no result"""
        self._execute(query, params)

    def execute_query_result(self, query: str, params: dict | list[dict] = None, return_list: bool = True) -> list[dict] | dict[list]:
        """Execute query with params, with result"""
        result = self._execute(query, params, _result=True)
        keys = list(result.keys())
        values = result.all()

        if return_list:
            return [{keys[i]: value[i] for i in range(len(keys))} for value in values]
        else:
            return {keys[i]: [value[i] for value in values] for i in range(len(keys))}

    def execute_query_result_single(self, query: str, params: dict | list[dict] = None) -> dict:
        """Execute query with params, with single result"""
        result = self._execute(query, params, _result=True)
        keys = list(result.keys())
        values = result.fetchone()

        if not values or result.fetchone():
            raise ValueError("Incorrect number of rows returned")

        result.close()
        return {keys[i]: values[0] for i in range(len(keys))}

    def _execute(self, query: str, params: dict | list[dict] = None, _result: bool = False) -> None | CursorResult:
        """Execute query with params, Privately"""
        with self._engine.connect() as connection:
            cur = connection.execute(sqlalchemy.text(query), params)

            if _result:
                return cur
            else:
                cur.close()

    def create_database(self):
        """Create database if not exists"""
        if not sqlalchemy_utils.database_exists(self._engine.url):
            sqlalchemy_utils.create_database(self._engine.url)

    def drop_database(self):
        """Drop database if not exists"""
        if sqlalchemy_utils.database_exists(self._engine.url):
            sqlalchemy_utils.drop_database(self._engine.url)

    def verify(self):
        """Check connection works"""
        if not self._engine:
            raise ValueError("The engine is not defined")

        if not sqlalchemy_utils.database_exists(self._engine.url):
            raise ValueError("The database is not defined")

        with self._engine.connect():
            pass
