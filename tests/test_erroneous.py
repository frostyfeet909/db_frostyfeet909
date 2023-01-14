import pytest
from sqlalchemy.exc import ArgumentError


@pytest.fixture
def url_erroneous_one():
    return "test"


@pytest.fixture
def url_erroneous_two():
    return "postgresql+psycopg2://{USERNAME}:{PASSWORD}@{IP}/{DATABASE}"


def test_connection_failure(url_erroneous_one, url_erroneous_two):
    from src import db_frostyfeet909 as db

    with pytest.raises(ArgumentError):
        db.Connection(url_erroneous_one)

    con = db.Connection(url_erroneous_two)

    with pytest.raises(Exception):
        con.verify()
