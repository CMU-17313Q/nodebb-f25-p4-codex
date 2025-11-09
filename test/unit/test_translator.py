from src.translator import translate_content

def test_german():
    is_en, text = translate_content("Dies ist eine Nachricht auf Deutsch")
    assert is_en is False
    assert text == "This is a German message"

def test_english_passthrough():
    is_en, text = translate_content("This is an English message")
    assert is_en is True
    assert text == "This is an English message"

def test_unknown_passthrough():
    is_en, text = translate_content("random abc")
    assert is_en is True
    assert text == "random abc"
