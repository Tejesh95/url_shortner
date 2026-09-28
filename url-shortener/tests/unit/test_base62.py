from app.utils.base62 import decode_base62, encode_base62


def test_known_values():
    assert encode_base62(0) == "0"
    assert encode_base62(125) == "21"
    assert encode_base62(1_000_000) == "4c92"


def test_round_trip():
    for number in [0, 1, 10, 61, 62, 125, 1_000_000, 1_000_000_000]:
        assert decode_base62(encode_base62(number)) == number
