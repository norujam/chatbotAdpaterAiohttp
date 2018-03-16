import configparser
from pymongo import MongoClient

CONFIG = configparser.ConfigParser()
CONFIG.read('config.properties')


class MongoDb:
    def __init__(self):
        self.db_client = None

    @staticmethod
    def connect_db():
        MongoDb.db_client = MongoClient(
            host=CONFIG['DB']['host'],
            port=int(CONFIG['DB']['port']),
            username=CONFIG['DB']['username'],
            password=CONFIG['DB']['password'],
            authSource=CONFIG['DB']['authSource'],
            maxPoolSize=50,
        )
        db_collect = MongoDb.db_client['django']
        return db_collect

    @staticmethod
    def close_db():
        try:
            MongoDb.db_client.close()
        except NameError:
            pass

    @staticmethod
    def save_data(col, data):
        try:
            db_collect = MongoDb.connect_db()
            db_collect.eval(col).insert_one(data)
        finally:
            MongoDb.close_db()
