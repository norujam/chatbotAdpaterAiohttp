from mongoengine import *
import configparser

config = configparser.ConfigParser()
config.read('config.properties')


class MongoDb:
    @staticmethod
    def connect_db():
        global db
        try:
            db = connect(
                db=config['DB']['db'],
                host=config['DB']['host'],
                port=int(config['DB']['port']),
                username=config['DB']['username'],
                password=config['DB']['password'],
                authSource=config['DB']['authSource'],
                maxPoolSize=50,
            )
        except Exception as err:
            raise err

    @staticmethod
    def close_db():
        try:
            global db
            db.close
        except NameError:
            pass

    @staticmethod
    def insert_document(obj_doc):
        try:
            MongoDb.connect_db()
            obj_doc.save()
        except Exception as err:
            raise err
        finally:
            MongoDb.close_db()
