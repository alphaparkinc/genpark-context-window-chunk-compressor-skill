"""Context Window Token Compressor & Saliency Scorer.
100% Python Standard Library.
"""

import math
import re

class ContextChunkCompressor:
    """Context window compressor using sentence saliency scoring and length budget."""
    @staticmethod
    def score_sentence(sentence, query_terms):
        words = set(re.findall(r'\b\w+\b', sentence.lower()))
        match_count = sum(1 for q in query_terms if q in words)
        length_penalty = 1.0 / (1.0 + math.log(max(len(words), 1)))
        return match_count * length_penalty

    @classmethod
    def compress(cls, context, query, max_chars=300):
        query_terms = set(re.findall(r'\b\w+\b', query.lower()))
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', context) if s.strip()]
        scored = []
        for i, s in enumerate(sentences):
            score = cls.score_sentence(s, query_terms)
            scored.append((score, i, s))
        scored.sort(key=lambda x: x[0], reverse=True)
        selected = []
        cur_len = 0
        for score, i, s in scored:
            if cur_len + len(s) + 1 <= max_chars:
                selected.append((i, s))
                cur_len += len(s) + 1
        selected.sort(key=lambda x: x[0])
        return " ".join(s for _, s in selected)
