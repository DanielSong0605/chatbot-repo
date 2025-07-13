from langchain_core.tools import tool
from datetime import datetime


@tool
def add(a: int, b: int) -> int:
    """Add two integers.

    Args:
        a: First integer
        b: Second integer
    """
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers.

    Args:
        a: First integer
        b: Second integer
    """
    return a * b


@tool
def get_date() -> str:
    """Get the current date in the user's timezone."""

    return datetime.now().strftime("%a %b %d %Y")


@tool
def get_time() -> str:
    """Get the current time 24hr in the user's timezone in hours, minutes, seconds."""

    return datetime.now().strftime("%H:%M, %Ss")


all_tools = [add, multiply, get_date, get_time]
