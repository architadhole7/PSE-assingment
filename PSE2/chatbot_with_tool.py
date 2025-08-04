import os
import re
from dotenv import load_dotenv
import google.generativeai as genai
from calculator_tool import add, subtract, multiply, divide, modulo

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-1.5-flash")

#
def is_math_question(query):
    # Detect if user is asking a simple math operation
    keywords = ["add", "plus", "sum", "subtract", "minus", "difference",
                "multiply", "times", "product", "divide", "divided", "quotient",
                "mod", "remainder", "modulo", "%"]
    return any(word in query.lower() for word in keywords)

def extract_numbers(query):
    return list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", query)))

def handle_math(query):
    numbers = extract_numbers(query)
    q = query.lower()

    if len(numbers) != 2:
        return "Sorry, I can only solve basic two-number calculations."

    a, b = numbers

    if "add" in q or "plus" in q or "sum" in q:
        return add(a, b)
    elif "subtract" in q or "minus" in q or "difference" in q:
        return subtract(a, b)
    elif "multiply" in q or "times" in q or "product" in q:
        return multiply(a, b)
    elif "divide" in q or "divided" in q or "quotient" in q:
        return divide(a, b)
    elif "mod" in q or "remainder" in q or "modulo" in q or "%" in q:
        return modulo(a, b)
    else:
        return "Sorry, I didn't recognize the math operation."
def is_multi_task(query):
    query_lower = query.lower().strip()

    # General factual concepts
    fact_keywords = [
        "capital", "bird", "color", "president", "prime minister", "largest",
        "national", "who","where", "why", "when", "name", "use",
        "purpose", "meaning", "define", "function", "role", "job", "explain"
    ]

    # Basic math keywords
    math_keywords = [
        "add", "plus", "sum", "subtract", "minus", "difference","What is","How much",
        "multiply", "times", "product", "divide", "divided", "quotient","Solve"
        "mod", "remainder", "modulo", "%", "+", "-", "*", "/", "="
    ]

    # Indicators of multi-task structure
    connectors = [" and ", ",", " also ", " then ", "? and", "&", " as well as "]

    has_fact = any(word in query_lower for word in fact_keywords)
    has_math = any(word in query_lower for word in math_keywords)
    has_connector = any(c in query_lower for c in connectors)

    # Deny if query mixes fact + math, or compound structure
    if (has_math and has_fact) or (has_connector and (has_math or has_fact)):
        return True

    return False


def log_interaction(user, assistant):
    with open("interaction_log.txt", "a", encoding="utf-8") as f:
        f.write(f"User: {user}\nAssistant: {assistant}\n{'-'*40}\n")

def main():
    print(" Level 2 Bot (Calculator tool). Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        if is_multi_task(user_input):
            assistant = "Sorry, I can't handle multiple tasks in one question. Please ask one at a time."

        elif is_math_question(user_input):
            assistant = f" Used calculator tool.\nResult: {handle_math(user_input)}"
        else:
            response = model.generate_content(
                f"Answer the question clearly. Use step-by-step reasoning.\n\nQuestion: {user_input}"
            )
            assistant = response.text

        print(f"\nAssistant: {assistant}\n")
        log_interaction(user_input, assistant)


if __name__ == "__main__":
    main()


