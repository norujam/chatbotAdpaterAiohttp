from aiohttp import web
import setLogger, logging
import configparser

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

app = web.Application()
app.router.add_post('/chatbot/message/', message_handle)
web.run_app(app, port=8000)
