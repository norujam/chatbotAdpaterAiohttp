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
    # result = await googleDialog.detect_intent_texts([message])
    # logging.debug(result)
    return web.json_response(result)


async def web_hook_handle(request):
    json_data = json.loads(request.body.decode())
    action = str(json_data['result']['action']).split("-")
    json_data = json_data['result']['parameters']
    for key in json_data.keys():
        global pKey
        pKey = key
    logging.debug("web_hook parameter="+pKey)

    # url = ""
    # payload = {}
    url = config['service']['service_url']+action[2]+"/"
    payload = {"param": pKey}
    html = requests.post(url, data=payload)

    # logging.debug(html.text)
    return web.json_response(json.loads(html.text))


app = web.Application()
app.router.add_post('/chatbot/message/', message_handle)
app.router.add_post('/chatbot/web_hook/', web_hook_handle)
web.run_app(app, port=8000)
