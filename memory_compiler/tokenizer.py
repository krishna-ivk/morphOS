from __future__ import annotations

import re

from .interfaces import Tokenizer


class SimpleTokenizer(Tokenizer):
    _pattern = re.compile(r"\w+|[^\w\s]", re.UNICODE)

    def count_tokens(self, text: str) -> int:
        return len(self._pattern.findall(text))

    def encode(self, text: str) -> list[int]:
        return [sum(ord(char) for char in token) % 8192 for token in self._pattern.findall(text)]
