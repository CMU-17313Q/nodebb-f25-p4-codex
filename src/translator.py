import ollama
import json
import re

def translate(content: str) -> tuple[bool, str]:
    prompt = f"""
Analyze the following text and determine if it is in English or another language.

If the text is in English, respond with exactly:
{{"is_english": true, "translated_content": ""}}

If the text is NOT in English, translate it to English and respond with exactly:
{{"is_english": false, "translated_content": "YOUR TRANSLATION HERE"}}

Respond ONLY with valid JSON. 
No explanations. No thinking. No markdown. No extra text.
If you cannot comply, output exactly: {{"is_english": true, "translated_content": ""}}.

Text to analyze:
{content}
"""

    try:
        response = ollama.chat(
            model="deepseek-r1:8b",
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = response["message"]["content"].strip()

        # Try normal JSON parsing
        try:
            result = json.loads(response_text)
            return result.get("is_english", True), result.get("translated_content", "")
        except:
            pass

        # Try fallback JSON extraction
        json_match = re.search(
            r'\{[\s\S]*?"is_english"[\s\S]*?"translated_content"[\s\S]*?\}',
            response_text
        )

        if json_match:
            try:
                result = json.loads(json_match.group(0))
                return result.get("is_english", True), result.get("translated_content", "")
            except:
                pass

        print("Warning: Could not parse:", response_text)
        return True, ""

    except Exception as e:
        print("Error calling LLM:", e)
        return True, ""


def translate_content(content: str) -> tuple[bool, str]:
    return translate(content)



