#importing packages

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file, it contains API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Instantiate model
model = genai.GenerativeModel('models/gemini-1.5-flash')

# Function to build prompt

def build_prompt(user_input):
    return f"""
You are a smart assistant. You must always:
- Think step-by-step.
- Use clear structure (lists or bullet points).
- Refuse math questions and suggest using a calculator.

User Question: {user_input}
Assistant:"""

def ask_gemini(user_input):
    prompt = build_prompt(user_input)
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"

def main():
    print("Level 1 Bot \nType 'exit' to quit.")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        answer = ask_gemini(user_input)
        print(f"\nAssistant: {answer}")

if __name__ == "__main__":
    main()


