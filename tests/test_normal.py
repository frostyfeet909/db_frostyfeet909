import pytest


@pytest.fixture
def url():
    from os import environ
    from dotenv import load_dotenv
    load_dotenv()
    return environ.get("DB_CONN") + "/test"


@pytest.fixture
def url_repeat(url):
    return url + "_repeat"


@pytest.fixture
def connection(url):
    from src import db_frostyfeet909 as db
    con = db.Connection(url)
    con.create_database()

    yield con

    con.drop_database()


@pytest.fixture
def connection_repeat(url):
    from src import db_frostyfeet909 as db
    con = db.Connection(url)
    con.create_database()

    yield con

    con.drop_database()


def test_connection(connection):
    assert connection.verify()


def test_utils(connection):
    assert connection.exists_database()
    connection.drop_database()
    assert not connection.drop_database()


def test_multi_connection(connection, connection_repeat):
    assert connection != connection_repeat
    assert connection.verify()
    assert connection_repeat.verify()
    assert connection._engine == connection_repeat._engine


def test_multi_import(url):
    from src import db_frostyfeet909 as db
    from src import db_frostyfeet909 as db_repeat

    connection = db.Connection(url)
    connection_repeat = db_repeat.Connection(url)

    from src import db_frostyfeet909 as db
    from src import db_frostyfeet909 as db_repeat

    assert connection._engine == connection_repeat._engine
    assert len(db.main.ENGINE) == 1
    assert db.main.ENGINE == db_repeat.main.ENGINE


def test_multi_engine(url, url_repeat):
    from src import db_frostyfeet909 as db
    connection = db.Connection(url)
    connection_repeat = db.Connection(url_repeat)
    connection_same = db.Connection(url)

    assert connection != connection_repeat and connection != connection_same
    assert connection._engine != connection_repeat._engine
    assert connection._engine == connection_same._engine
    assert len(db.main.ENGINE) == 2
