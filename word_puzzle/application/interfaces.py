"""
Application Layer Interfaces (Ports)
Define abstract interfaces that outer layers must implement
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from ..domain import Puzzle, Word


class IPuzzleRepository(ABC):
    """Interface for puzzle persistence."""

    @abstractmethod
    def save(self, puzzle: Puzzle, filename: str) -> None:
        """Save a puzzle to persistent storage."""
        pass


class IWordRepository(ABC):
    """Interface for word data access."""

    @abstractmethod
    def get_default_words(self) -> List[Word]:
        """Get default word list."""
        pass

    @abstractmethod
    def load_from_file(self, filepath: str) -> List[Word]:
        """Load words from a file."""
        pass


class IPuzzlePresenter(ABC):
    """Interface for presenting puzzle data."""

    @abstractmethod
    def present(self, puzzles: List[Puzzle], metadata: Dict[str, Any]) -> Any:
        """Present puzzle data in a specific format."""
        pass


class IConfigValidator(ABC):
    """Interface for validating puzzle configuration."""

    @abstractmethod
    def validate_grid_size(self, size: int) -> None:
        """Validate grid size."""
        pass

    @abstractmethod
    def validate_words(self, words: List[Word], grid_size: int) -> None:
        """Validate word list against grid size."""
        pass
