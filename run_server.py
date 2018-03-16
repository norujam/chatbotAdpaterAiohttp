import logging
import configparser
import json
import traceback
import requests
import setLogger
from aiohttp import web
from chatbot import do_not_call_api

CONFIG = configparser.ConfigParser()
CONFIG.read('config.properties')


def main():
    logging.debug("init service")


if __name__ == '__main__':
    main()


async def message_handle(request):
    try:
        message = (await request.post())['message']
        result = do_not_call_api.check_message(message)
        if result is None:
            api_call_module = __import__(CONFIG['setSite']['apiCallModule'],
                                         fromlist=["detect_intent_texts"])
            result = await api_call_module.detect_intent_texts([message])
            if any(result["action"].find(s) > -1 for s in ['outer_retrieve', 'outer_response']):
                result["result"] = await web_hook(result)

        # result = await googleDialog.detect_intent_texts([message])
        logging.debug(result)
    except Exception as err:
        logging.error(err)
        traceback.print_exc()

    return web.json_response(result)


async def web_hook(result):
    try:
        action = result['action'].split("_")
        parameters = result['parameters']
        payload = {}
        for key in parameters.keys():
            payload[key] = parameters[key]
        # url = ""
        # payload = {}

        url = CONFIG['service']['service_url']+action[2]+"/"
        html = requests.post(url, data=payload)
        logging.debug(html)
    except Exception as err:
        logging.error(err)
        raise err

    return json.loads(html.text)["result"]

app = web.Application()
app.router.add_post('/chatbot/message/', message_handle)
web.run_app(app, port=8000)
