# translator_tool.py

from googletrans import Translator

translator = Translator()

def translate(text, target_language):
    try:
        result = translator.translate(text, dest=target_language)
        return result.text
    except Exception as e:
        return f"Translation error: {e}"
