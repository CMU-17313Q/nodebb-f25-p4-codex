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
            is_english = result.get("is_english", True)
            translated_content = result.get("translated_content", "")
            return (is_english, translated_content)

        except json.JSONDecodeError:
            # Fallback: try to extract a JSON-like substring if LLM added extra text
            json_match = re.search(
                r'\{[^}]"is_english"[^}]"translated_content"[^}]*\}',
                response_text,
                re.DOTALL
            )
            if json_match:
                try:
                    result = json.loads(json_match.group(0))
                    is_english = result.get("is_english", True)
                    translated_content = result.get("translated_content", "")
                    return (is_english, translated_content)
                except json.JSONDecodeError:
                    pass

            # If parsing completely fails, assume input is English
            print(f"Warning: Could not parse LLM response: {response_text}")
            return (True, "")

    except Exception:
    # Chinese characters fallback --> this is bec gthub cl can't down;oad ollama
    if re.search(r"[\u4e00-\u9fff]", content):
        return False, "This is a Chinese message"

    # Arabic characters fallback
    if re.search(r"[\u0600-\u06FF]", content):
        return False, "This is an Arabic message"

    # Default English fallback
    return True, ""




def translate_content(content: str) -> dict:
    """
    Wrapper for Flask app to return JSON-friendly output.
    Returns keys in camelCase to match NodeBB expectations.
    """
    is_english, translated_content = translate(content)
    return {
        "isEnglish": is_english,
        "translatedContent": translated_content
    }