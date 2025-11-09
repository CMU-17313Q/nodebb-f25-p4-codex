import pytest
from unittest.mock import patch
from src.translator import query_llm_robust
from ollama import Client

# Use same client config used by translator.py
client = Client(host="localhost:11434")


# ----------------------------------------------------
# Test 1 – weird / unexpected language output
# ----------------------------------------------------
@patch.object(client, "chat")
def test_unexpected_language(mock_chat):

    class FakeMsg:
        content = "I don't understand your request"

    class FakeResp:
        message = FakeMsg()

    mock_chat.return_value = FakeResp()

    result = query_llm_robust("Hier ist dein erstes Beispiel.")

    assert isinstance(result, tuple)
    assert isinstance(result[0], bool)
    assert isinstance(result[1], str)


# ----------------------------------------------------
# Test 2 – translation call raises an error
# ----------------------------------------------------
@patch.object(client, "chat")
def test_translation_failure(mock_chat):

    def fake_chat_side_effect(*args, **kwargs):
        class FakeMsg:
            def __init__(self, text):
                self.content = text

        class FakeResp:
            def __init__(self, text):
                self.message = FakeMsg(text)

        # First call = language detection
        if not hasattr(fake_chat_side_effect, "called"):
            fake_chat_side_effect.called = True
            return FakeResp("German")

        # Second call = blow up
        raise Exception("translation failed")

    mock_chat.side_effect = fake_chat_side_effect

    result = query_llm_robust("Guten Morgen")

    assert isinstance(result, tuple)
    assert isinstance(result[0], bool)
    assert isinstance(result[1], str)


# ----------------------------------------------------
# Test 3 – language output is malformed (non-string)
# ----------------------------------------------------
@patch.object(client, "chat")
def test_bad_language_output(mock_chat):

    class FakeMsg:
        content = 12345  # invalid

    class FakeResp:
        message = FakeMsg()

    mock_chat.return_value = FakeResp()

    result = query_llm_robust("Bonjour")

    assert isinstance(result, tuple)
    assert isinstance(result[0], bool)
    assert isinstance(result[1], str)


# ----------------------------------------------------
# Test 4 – translation returns empty string
# ----------------------------------------------------
@patch.object(client, "chat")
def test_empty_translation(mock_chat):

    responses = ["French", ""]

    def fake_chat(*args, **kwargs):
        text = responses.pop(0)

        class FakeMsg:
            def __init__(self, c):
                self.content = c

        class FakeResp:
            def __init__(self, c):
                self.message = FakeMsg(c)

        return FakeResp(text)

    mock_chat.side_effect = fake_chat

    result = query_llm_robust("Bonjour tout le monde")

    assert isinstance(result, tuple)
    assert isinstance(result[0], bool)
    assert isinstance(result[1], str)
