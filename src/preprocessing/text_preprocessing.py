"""
Text & Symptom Preprocessing for VitalLens.
Produces tokens AND common medical phrase n-grams so the NLP model
can match both single keywords and multi-word symptom phrases.
"""

from typing import List
import re


def preprocess_symptoms(text: str) -> List[str]:
    """
    Returns a list of tokens + 2/3-gram phrases from symptom text.

    Process:
      1. Lowercase and clean punctuation
      2. Generate unigrams, bigrams, and trigrams
      3. Deduplicate while preserving order

    The NLP model uses substring matching on ' '.join(tokens), so
    including reconstructed phrases improves multi-word keyword detection.
    """
    if not text:
        return []

    # Lowercase and collapse whitespace/punctuation to spaces
    cleaned = re.sub(r"[^a-zA-Z\s]", " ", text.lower())
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    words = [w for w in cleaned.split() if len(w) > 1]

    tokens: List[str] = list(words)  # unigrams

    # Bigrams
    for i in range(len(words) - 1):
        tokens.append(f"{words[i]} {words[i+1]}")

    # Trigrams
    for i in range(len(words) - 2):
        tokens.append(f"{words[i]} {words[i+1]} {words[i+2]}")

    # Deduplicate, preserve order
    seen = set()
    unique = []
    for t in tokens:
        if t not in seen:
            seen.add(t)
            unique.append(t)

    return unique
