ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
BASE = len(ALPHABET)


def encode_base62(value: int, min_length: int = 1) -> str:
    if value < 0:
        raise ValueError("value must be non-negative")

    if value == 0:
        encoded = ALPHABET[0]
    else:
        chars: list[str] = []
        while value:
            value, remainder = divmod(value, BASE)
            chars.append(ALPHABET[remainder])
        encoded = "".join(reversed(chars))

    return encoded.rjust(min_length, ALPHABET[0])


def decode_base62(code: str) -> int:
    if not code:
        raise ValueError("code must not be empty")

    value = 0
    for char in code:
        value = value * BASE + ALPHABET.index(char)
    return value
