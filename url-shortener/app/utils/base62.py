from app.core.constants import BASE62_ALPHABET


def encode_base62(number: int) -> str:
    if number < 0:
        raise ValueError("number must be non-negative")
    if number == 0:
        return "0"

    chars = []
    base = len(BASE62_ALPHABET)
    while number:
        number, remainder = divmod(number, base)
        chars.append(BASE62_ALPHABET[remainder])
    return "".join(reversed(chars))


def decode_base62(value: str) -> int:
    if not value:
        raise ValueError("value must not be empty")

    lookup = {char: index for index, char in enumerate(BASE62_ALPHABET)}
    number = 0
    for char in value:
        if char not in lookup:
            raise ValueError("invalid Base62 character")
        number = number * 62 + lookup[char]
    return number
