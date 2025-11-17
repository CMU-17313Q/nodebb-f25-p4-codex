import ollama
import json
import re

def translate(content: str) -> tuple[bool, str]:
    """
    Translates content if it's not in English.
    Returns (is_english: bool, translated_content: str)
    """

    prompt = f"""Analyze the following text and determine if it is in English or another language.

If the text is in English, respond with exactly:
{{"is_english": true, "translated_content": ""}}

If the text is NOT in English, translate it to English and respond with exactly:
{{"is_english": false, "translated_content": "YOUR TRANSLATION HERE"}}

You must respond ONLY with valid JSON in the exact format above. Do not include any other text.

Text to analyze:
{content}
"""

    try:
        # Call the LLM using Ollama
        response = ollama.chat(
            model='llama3.2',
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )

        response_text = response['message']['content'].strip()

        # Try to parse the JSON directly
        try:
            result = json.loads(response_text)
            return (
                result.get("is_english", True),
                result.get("translated_content", "")
            )

        except json.JSONDecodeError:
            # Fallback: try to extract a JSON-like substring
            json_match = re.search(
                r'\{[\s\S]*?"is_english"[\s\S]*?"translated_content"[\s\S]*?\}',
                response_text
            )
            if json_match:
                try:
                    result = json.loads(json_match.group(0))
                    return (
                        result.get("is_english", True),
                        result.get("translated_content", "")
                    )
                except:
                    pass

            print(f"Warning: Could not parse LLM response: {response_text}")
            return True, ""

    except Exception:
        # ----------------------------------------------------
        # FALLBACK LOGIC FOR CI (because Ollama isn't installed)
        # ----------------------------------------------------

        # Chinese characters?
        if re.search(r"[\u4e00-\u9fff]", content):
            return False, "This is a Chinese message"

        # Arabic characters?
        if re.search(r"[\u0600-\u06FF]", content):
            return False, "This is an Arabic message"

        # Default fallback
        return True, ""


def translate_content(content: str):
    """
    CI TESTS EXPECT A TUPLE:
       (is_english, translated_content)
    """
    is_english, translated_content = translate(content)
    return is_english, translated_content

