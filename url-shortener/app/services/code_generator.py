from app.cache.counter import Counter
from app.utils.base62 import encode_base62


class CodeGenerator:
    def __init__(self, counter: Counter):
        self.counter = counter

    def generate(self) -> tuple[str, int]:
        generated_id = self.counter.next_id()
        return encode_base62(generated_id), generated_id
