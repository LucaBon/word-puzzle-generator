"""
Infrastructure Layer - Repository Implementations
These implement the interfaces defined in the application layer
"""
import sys
from typing import List, Any
from ..domain import Word
from ..application.interfaces import IWordRepository, IPuzzleRepository


class FileWordRepository(IWordRepository):
    """Repository for loading words from files and defaults."""

    DEFAULT_WORDS = [
        "addobbo", "angelo", "giuseppe", "cometa", "stella", "maria",
        "magi", "betlemme", "bue", "natale", "asinello", "stalla"
    ]

    def get_default_words(self) -> List[Word]:
        """Get default Christmas-themed words."""
        print("✓ Using default Christmas-themed words")
        return [Word(w) for w in self.DEFAULT_WORDS]

    def load_from_file(self, filepath: str) -> List[Word]:
        """Load words from a text file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                word_strings = [line.strip() for line in f if line.strip()]
            words = [Word(w) for w in word_strings]
            print(f"✓ Loaded {len(words)} words from {filepath}")
            return words
        except FileNotFoundError:
            print(f"✗ Error: File '{filepath}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"✗ Error reading file: {e}")
            sys.exit(1)


class HTMLFileRepository(IPuzzleRepository):
    """Repository for saving puzzles as HTML files."""

    def save(self, content: Any, filename: str) -> None:
        """Save HTML content to a file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"\n✓ Interactive HTML file exported: {filename}")
        except Exception as e:
            print(f"✗ Error saving file: {e}")
            sys.exit(1)
