import re


def valid_email(text) -> bool:
    if not re.match(r'[^@]+@[^@]+\.[^@]+', text):
        return False

    return True


def valid_password(text) -> bool:
    if len(text) < 12 or not any(char.isdigit() for char in text) or not any(char.isalpha() for char in text):
        return False

    return True


def valid_url(text) -> bool:
    if not re.match(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})', text):
        return False

    return True
