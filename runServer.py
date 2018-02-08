from aiohttp import web
from chatbot import googleDialog
from chatbot.chatDataObjectMap import ChatDataObjectMap
import setLogger, logging, asyncio

def main():
    logging.debug("init service")

if __name__ == '__main__':
    main()


async def messageHandle(request):
    message = (await request.post())['message']
    result = await googleDialog.detectIntentTexts([message])
    logging.debug(result)
    return web.json_response(result)

app = web.Application()
app.router.add_post('/chatbot/message/', messageHandle)
web.run_app(app, port=8000)
