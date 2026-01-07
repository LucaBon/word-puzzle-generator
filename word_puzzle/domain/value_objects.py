"""
Domain Value Objects - Immutable objects without identity
Value objects are compared by their values, not by identity
"""
from dataclasses import dataclass
from typing import List
from enum import Enum


@dataclass(frozen=True)
class Position:
    """Immutable position in the grid."""
    row: int
    col: int

    def __str__(self) -> str:
        return f"({self.row}, {self.col})"


@dataclass(frozen=True)
class Direction:
    """Immutable direction for word placement."""
    row_delta: int
    col_delta: int
    name: str

    def __str__(self) -> str:
        return self.name

    def is_horizontal(self) -> bool:
        """Check if this is a horizontal direction."""
        return 'horizontal' in self.name.lower()

    def is_vertical(self) -> bool:
        """Check if this is a vertical direction."""
        return 'vertical' in self.name.lower()

    def is_diagonal(self) -> bool:
        """Check if this is a diagonal direction."""
        return 'diagonal' in self.name.lower()


class DirectionType(Enum):
    """Enumeration of direction categories."""
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    DIAGONAL = "diagonal"


@dataclass(frozen=True)
class Word:
    """Immutable word value object."""
    value: str

    def __post_init__(self):
        """Validate and normalize the word."""
        if not self.value:
            raise ValueError("Word cannot be empty")
        # Force uppercase through object.__setattr__ since frozen=True
        object.__setattr__(self, 'value', self.value.upper())

    def __len__(self) -> int:
        return len(self.value)

    def __str__(self) -> str:
        return self.value

    def __getitem__(self, index: int) -> str:
        return self.value[index]


@dataclass(frozen=True)
class GridSize:
    """Value object representing grid dimensions."""
    value: int

    def __post_init__(self):
        """Validate grid size."""
        if self.value < 5:
            raise ValueError("Grid size must be at least 5")
        if self.value > 30:
            raise ValueError("Grid size must be at most 30")

    def __int__(self) -> int:
        return self.value


# Predefined directions
class Directions:
    """Factory for creating standard directions."""
    HORIZONTAL_RIGHT = Direction(0, 1, 'horizontal_right')
    HORIZONTAL_LEFT = Direction(0, -1, 'horizontal_left')
    VERTICAL_DOWN = Direction(1, 0, 'vertical_down')
    VERTICAL_UP = Direction(-1, 0, 'vertical_up')
    DIAGONAL_DOWN_RIGHT = Direction(1, 1, 'diagonal_down_right')
    DIAGONAL_DOWN_LEFT = Direction(1, -1, 'diagonal_down_left')
    DIAGONAL_UP_RIGHT = Direction(-1, 1, 'diagonal_up_right')
    DIAGONAL_UP_LEFT = Direction(-1, -1, 'diagonal_up_left')

    @classmethod
    def all(cls) -> List[Direction]:
        """Get all available directions."""
        return [
            cls.HORIZONTAL_RIGHT, cls.HORIZONTAL_LEFT,
            cls.VERTICAL_DOWN, cls.VERTICAL_UP,
            cls.DIAGONAL_DOWN_RIGHT, cls.DIAGONAL_DOWN_LEFT,
            cls.DIAGONAL_UP_RIGHT, cls.DIAGONAL_UP_LEFT
        ]

    @classmethod
    def horizontal(cls) -> List[Direction]:
        """Get all horizontal directions."""
        return [cls.HORIZONTAL_RIGHT, cls.HORIZONTAL_LEFT]

    @classmethod
    def vertical(cls) -> List[Direction]:
        """Get all vertical directions."""
        return [cls.VERTICAL_DOWN, cls.VERTICAL_UP]

    @classmethod
    def diagonal(cls) -> List[Direction]:
        """Get all diagonal directions."""
        return [
            cls.DIAGONAL_DOWN_RIGHT, cls.DIAGONAL_DOWN_LEFT,
            cls.DIAGONAL_UP_RIGHT, cls.DIAGONAL_UP_LEFT
        ]

    @classmethod
    def by_type(cls, direction_type: DirectionType) -> List[Direction]:
        """Get directions by type."""
        if direction_type == DirectionType.HORIZONTAL:
            return cls.horizontal()
        elif direction_type == DirectionType.VERTICAL:
            return cls.vertical()
        elif direction_type == DirectionType.DIAGONAL:
            return cls.diagonal()
        else:
            return cls.all()
