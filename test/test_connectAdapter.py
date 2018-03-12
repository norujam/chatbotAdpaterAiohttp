import pytest
import aiohttp
import configparser
import requests

config = configparser.ConfigParser()
config.read('config.properties')


class TestConnectAdapter(object):

    def test_http_service(self):
        try:
            url = config['service']['service_url']
            html = requests.post(url, data=None)
        except ConnectionError:
            assert False

    @pytest.mark.asyncio
    async def test_http_client(self):
        async with aiohttp.ClientSession() as session:
            async with session.post("http://127.0.0.1:8000/chatbot/message/", data={'message': '오늘은 몇일이지?'}) as resp:
                assert resp.status == 200
