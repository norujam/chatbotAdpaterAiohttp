from pymongo import *
import configparser
import datetime

config = configparser.ConfigParser()
config.read('config.properties')


class MongoDb:
    @staticmethod
    def connect_db():
        global client
        client = MongoClient(
            host=config['DB']['host'],
            port=int(config['DB']['port']),
            username=config['DB']['username'],
            password=config['DB']['password'],
            authSource=config['DB']['authSource'],
            maxPoolSize=50,
        )
        db = client['django']
        return db

    @staticmethod
    def close_db():
        try:
            global client
            client.close()
        except NameError:
            pass

    @staticmethod
    def save_data(col, data):
        try:
            db = MongoDb.connect_db()
            db.eval(col).insert_one(data)
        finally:
            MongoDb.close_db()
