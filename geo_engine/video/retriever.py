"""
Video transcript chunk retriever.
Finds most relevant timestamped chunks for a query using keyword and term overlap scoring within strict token budgets.
"""

import math
import re
from typing import List
from geo_engine.video.indexer import VideoChunk


class VideoRetriever:
    """Retrieves the most salient timestamped video chunks for a given analytical query."""

    STOPWORDS = {
        "a", "an", "the", "and", "or", "but", "if", "then", "of", "to", "in",
        "on", "at", "by", "for", "with", "about", "is", "are", "was", "were",
        "it", "this", "that", "these", "those", "what", "how", "why", "when", "where"
    }

    @classmethod
    def _tokenize(cls, text: str) -> List[str]:
        words = re.findall(r"\b[a-zA-Z0-9_\-]+\b", text.lower())
        return [w for w in words if w not in cls.STOPWORDS and len(w) > 1]

    @classmethod
    def score_chunk(cls, chunk: VideoChunk, query_tokens: List[str]) -> float:
        """Calculates keyword relevance score based on query term matches and frequency."""
        if not query_tokens:
            return 0.0

        chunk_tokens = cls._tokenize(chunk.text)
        if not chunk_tokens:
            return 0.0

        score = 0.0
        token_set = set(chunk_tokens)
        for q in query_tokens:
            matches = chunk_tokens.count(q)
            if matches > 0:
                # Sub-linear term frequency weighting
                score += (1.0 + math.log(matches)) * 1.5
            elif any(q in t or t in q for t in token_set if len(t) > 3 and len(q) > 3):
                # Substring/partial match bonus
                score += 0.5

        return score

    @classmethod
    def retrieve(
        cls,
        chunks: List[VideoChunk],
        query: str,
        top_k: int = 3,
        max_total_tokens: int = 800
    ) -> List[VideoChunk]:
        """
        Scores all chunks against query, ranks them, and selects top-k chunks
        without exceeding max_total_tokens.
        """
        if not chunks:
            return []

        query_tokens = cls._tokenize(query)
        scored_chunks = []
        for chunk in chunks:
            score = cls.score_chunk(chunk, query_tokens)
            scored_chunks.append((score, chunk))

        # Sort by score descending, then earlier timestamp ascending
        scored_chunks.sort(key=lambda x: (x[0], -x[1].start_time), reverse=True)

        selected: List[VideoChunk] = []
        accumulated_tokens = 0

        for score, chunk in scored_chunks:
            if len(selected) >= top_k:
                break
            # Always take at least one if available
            if selected and (accumulated_tokens + chunk.token_estimate > max_total_tokens):
                continue
            selected.append(chunk)
            accumulated_tokens += chunk.token_estimate

        # Return in chronological order for coherent narrative synthesis
        selected.sort(key=lambda c: c.start_time)
        return selected
