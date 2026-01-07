"""
Infrastructure Layer - Validators
Concrete implementations of validation logic
"""
import sys
from typing import List
from ..domain import Word
from ..application.interfaces import IConfigValidator


class PuzzleConfigValidator(IConfigValidator):
    """Validates puzzle configuration parameters."""

    MIN_GRID_SIZE = 5
    MAX_GRID_SIZE = 30

    def validate_grid_size(self, size: int) -> None:
        """Validate grid size is within acceptable bounds."""
        if size < self.MIN_GRID_SIZE:
            raise ValueError(f"Grid size must be at least {self.MIN_GRID_SIZE}")

        if size > self.MAX_GRID_SIZE:
            raise ValueError(f"Grid size must be at most {self.MAX_GRID_SIZE}")

    def validate_words(self, words: List[Word], grid_size: int) -> None:
        """Validate that words list is not empty and words fit in grid."""
        if len(words) == 0:
            raise ValueError("No words provided")

        max_word_length = max(len(word) for word in words)
        if max_word_length > grid_size:
            longest_word = max(words, key=len)
            raise ValueError(
                f"Longest word '{longest_word}' ({max_word_length} letters) "
                f"won't fit in {grid_size}x{grid_size} grid. "
                f"Increase grid size to at least {max_word_length} or use shorter words."
            )
