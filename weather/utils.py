import re


def is_russian(text: str) -> bool:
    """Checking for Russian letters"""
    return bool(re.match(r"^[а-яА-ЯёЁ\s]+$", text))
