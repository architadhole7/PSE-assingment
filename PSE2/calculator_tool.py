# calculator_tool.py

"""
This module defines basic arithmetic functions used by the chatbot.
The chatbot will call these functions to perform calculations instead of the LLM answering them directly.
Supported operations: addition, subtraction, multiplication, division, modulo (remainder).
"""

def add(a, b):
    """Return the sum of two numbers."""
    return a + b

def subtract(a, b):
    """Return the difference between two numbers."""
    return a - b

def multiply(a, b):
    """Return the product of two numbers."""
    return a * b

def divide(a, b):
    """Return the quotient of two numbers. Handles division by zero."""
    if b == 0:
        return "Error: Division by zero."
    return a / b

def modulo(a, b):
    """Return the remainder of the division between two numbers."""
    if b == 0:
        return "Error: Division by zero."
    return a % b
