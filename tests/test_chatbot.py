import pytest
import asyncio
from chatbot import Chatbot

@pytest.fixture
def chatbot():
    return Chatbot()

@pytest.mark.asyncio
async def test_search_internet(chatbot):
    query = "Python programming"
    urls = await chatbot.search_internet(query)
    assert isinstance(urls, list)
    assert len(urls) <= 5
    assert all(isinstance(url, str) for url in urls)
    assert all(url.startswith('http') for url in urls)

@pytest.mark.asyncio
async def test_extract_text(chatbot):
    url = "https://python.org"
    text = await chatbot.extract_text(url)
    assert isinstance(text, str)
    assert len(text) > 0

@pytest.mark.asyncio
async def test_get_ai_response(chatbot):
    user_input = "What is Python?"
    context = "Python is a programming language"
    response = await chatbot.get_ai_response(user_input, context)
    assert isinstance(response, str)
    assert len(response) > 0

@pytest.mark.asyncio
async def test_conversation_history(chatbot):
    user_input = "Tell me about Python"
    await chatbot.process_user_input(user_input)
    assert len(chatbot.conversation_history) > 0
    assert isinstance(chatbot.conversation_history, list)
    assert all(isinstance(msg, dict) for msg in chatbot.conversation_history)

@pytest.mark.asyncio
async def test_conversation_history_limit(chatbot):
    for i in range(6):
        await chatbot.process_user_input(f"Test message {i}")
    assert len(chatbot.conversation_history) <= 10

@pytest.mark.asyncio
async def test_api_keys_loaded():
    from chatbot import OPENAI_API_KEY, SERPER_API_KEY
    assert OPENAI_API_KEY is not None
    assert OPENAI_API_KEY.startswith('sk-')
    assert SERPER_API_KEY is not None
