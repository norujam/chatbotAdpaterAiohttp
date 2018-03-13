import configparser
import asynctest
from chatbot import googleDialog


class GoogleDialogTest(asynctest.TestCase):

    async def test_call_case1(self):
        result = await googleDialog.detect_intent_texts(["오늘은 몇일인가요?"])
        self.assertIsNotNone(result)

    async def test_call_case2(self):
        result = await googleDialog.detect_intent_texts(["유럽에 대한 정보를 알려줘요"])
        self.assertIsNotNone(result)


if __name__ == '__main__':
    asynctest.main()
