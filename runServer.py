from aiohttp import web
import setLogger, logging
import configparser
import json
import requests

config = configparser.ConfigParser()
config.read('config.properties')


def main():
    logging.debug("init service")


if __name__ == '__main__':
    main()


async def message_handle(request):
    message = (await request.post())['message']
    api_call_module = __import__(config['setSite']['apiCallModule'], fromlist=["detect_intent_texts"])
    result = await api_call_module.detect_intent_texts([message])
    if any(s.find(result["action"]) for s in ['outer_retrieve', 'outer_response']):
        response_result = await web_hook(result)
    # result = await googleDialog.detect_intent_texts([message])
    # logging.debug(result)

    return web.json_response(result)


async def web_hook(result):
    action = result['action'].split("_")
    parameters = result['parameters']
    for key in parameters.keys():
        global pKey
        pKey = key
    # url = ""
    # payload = {}

    if any(s.find(result["action"]) for s in ['outer_response']):
        url = config['service']['service_url']+action[2]+"/"
        payload = {"paramKey": pKey, "paramValue": parameters[pKey]}
        html = requests.post(url, data=payload)

    # logging.debug(html.text)
    return web.json_response(json.loads(html.text))


app = web.Application()
app.router.add_post('/chatbot/message/', message_handle)
web.run_app(app, port=8000)
