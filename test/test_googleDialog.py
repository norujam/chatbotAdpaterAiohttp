from chatbot import googleDialog
import pytest


class TestGoogleDialog(object):

    @pytest.mark.asyncio
    async def test_call_case1(self):
        result = await googleDialog.detect_intent_texts("오늘은 몇일이지?")
        assert result["main_message"] is not None

    @pytest.mark.asyncio
    async def test_call_case2(self):
        result = await googleDialog.detect_intent_texts("유럽에 대한 정보를 알려줘요")
        assert result["main_message"] is not None
