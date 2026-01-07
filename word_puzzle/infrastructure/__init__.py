"""Infrastructure layer - External interfaces and implementations."""
from .repositories import FileWordRepository, HTMLFileRepository
from .validators import PuzzleConfigValidator

__all__ = [
    'FileWordRepository', 'HTMLFileRepository',
    'PuzzleConfigValidator'
]
