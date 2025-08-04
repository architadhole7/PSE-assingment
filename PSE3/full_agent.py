import os
import re
from dotenv import load_dotenv
from calculator_tool import add, subtract, multiply, divide, modulo, power
from translator_tool import translate
import google.generativeai as genai
from word2number import w2n

# Load Gemini API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Logging
def log_interaction(user, assistant):
    with open("interaction_log.txt", "a", encoding="utf-8") as f:
        f.write(f"User: {user}\nAssistant: {assistant}\n{'-'*40}\n")

# Math handler
def handle_math(query):
    q = query.lower()
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", q)

    if len(numbers) < 2:
        # Try to extract from text numbers
        try:
            words = q.split()
            numbers = [w2n.word_to_num(w) for w in words if w.isalpha()]
        except Exception:
            return "Please provide two valid numbers."

    if len(numbers) < 2:
        return "Please provide two valid numbers."

    a, b = float(numbers[0]), float(numbers[1])

    if "add" in q or "+" in q:
        return add(a, b)
    elif "subtract" in q or "minus" in q or "-" in q:
        return subtract(a, b)
    elif "multiply" in q or "times" in q or "*" in q:
        return multiply(a, b)
    elif "divide" in q or "/" in q:
        return divide(a, b)
    elif "mod" in q or "remainder" in q or "%" in q:
        return modulo(a, b)
    elif "power" in q or "raise" in q:
        return power(a, b)
    else:
        return "Unknown math operation."

# Translation handler
def handle_translation(task):
    match = re.search(r"translate ['\"](.+?)['\"](?: into)? (\w+)", task)
    if match:
        phrase = match.group(1)
        lang = match.group(2)
        return translate(phrase, lang)
    else:
        return "Please provide a phrase and target language to translate."

# Task splitter
def split_tasks(user_input):
    # Only split on 'then', 'also', 'and then' but NOT 'and' alone
    return [part.strip() for part in re.split(r"\b(?:then|also|and then)\b", user_input, flags=re.IGNORECASE)]

# Multi-task handler
def extract_subtasks(task):
    # Split within a task (like: "add 2 and 2 and multiply 3 and 3")
    matches = re.findall(r"(add|subtract|multiply|divide|mod|power|translate)[^add|subtract|multiply|divide|mod|power|translate]+", task, re.IGNORECASE)
    if matches:
        pieces = re.split(r"(?i)(?=add|subtract|multiply|divide|mod|power|translate)", task)
        return [p.strip() for p in pieces if p.strip()]
    return [task.strip()]

# Single-task processor
def process_task(task):
    task = task.strip().lower()

    if "translate" in task:
        return handle_translation(task)

    elif any(op in task for op in ["add", "subtract", "multiply", "divide", "mod", "power", "+", "-", "*", "/", "%"]):
        return f"Result: {handle_math(task)}"

    else:
        # Gemini fallback
        try:
            response = model.generate_content(f"Answer briefly: {task}")
            return response.text.strip()
        except Exception as e:
            return f"Gemini API error: {e}"

# Main agent loop
def main():
    print("🔴 Level 3 – Full Agentic AI Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        results = []
        steps = split_tasks(user_input)

        step_counter = 1
        for step in steps:
            subtasks = extract_subtasks(step)
            for sub in subtasks:
                result = process_task(sub)
                results.append(f"Step {step_counter}: {result}")
                step_counter += 1

        final_output = "\n".join(results)
        print(f"\nAssistant:\n{final_output}")
        log_interaction(user_input, final_output)

if __name__ == "__main__":
    main()
