import logging
from db.mongo_db import MongoDb
from models.chat_log import ChatLog


class ShortSentenceError(Exception):
    def __init__(self, sentence):
        super(ShortSentenceError, self).__init__(sentence)
        self.message = sentence
        logging.debug("no pattern/unknown short: "+sentence)


class ChatLogObjectMap:
    @staticmethod
    async def insert_log(param):
        try:
            if param["action"] == 'input.unknown' and len(param["text"][0]) < 5:
                raise ShortSentenceError(param["text"][0])

            chat_log = ChatLog(sentence=param["text"][0], actionType=param["action"])
            try:
                param_list = []
                for key in param["parameters"].keys():
                    param_list.append(param["parameters"][key])
                chat_log.keywords = param_list
            except KeyError:
                chat_log.keywords = []
            MongoDb.insert_document(chat_log)
        except ShortSentenceError:
            pass
        except Exception as err:
            logging.error(err)
            raise err
