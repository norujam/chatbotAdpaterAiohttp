from db.mongo_db_py_mongo import MongoDb
import pytest
import datetime


@pytest.fixture(scope="session")
def test_db_connection():
    try:
        global db
        db = MongoDb.connect_db()
        assert db is not None
    except ConnectionError:
        assert False


@pytest.fixture(scope="session")
def test_db_insert(test_db_connection):
    global db
    global col
    col = db.chat_log
    global data_id
    data_id = "test-13"
    result = col.insert_one({"_id": data_id, "actionType": "test", "sentence": "22", "keywords": ["11", "22"], "regDate": datetime.datetime.utcnow()})

    return result


def test_db(test_db_insert):
    try:
        global data_id
        test_db_insert
        col.remove({"_id": data_id})
    except Exception:
        assert False

