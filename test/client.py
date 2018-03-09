import aiohttp
import asyncio
import json


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post("http://127.0.0.1:8000/chatbot/message/", data={'message': '오늘은 몇일인가요?'}) as resp:
            print(resp.status)
            result = await resp.text()
            print(json.loads(result))

        async with session.post("http://127.0.0.1:8000/chatbot/message/", data={'message': '유럽에 대한 정보를 알려줘요'}) as resp:
            print(resp.status)
            result = await resp.text()
            print(json.loads(result))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
