"""
Domain Entities - Core business objects with identity
These are the heart of the application and contain business logic
"""
from dataclasses import dataclass, field
from typing import List, Tuple
from .value_objects import Position, Direction, Word


@dataclass
class WordPlacement:
    """Entity representing a word placed in the puzzle grid."""
    word: Word
    start_position: Position
    direction: Direction
    positions: List[Position] = field(default_factory=list)

    def __post_init__(self):
        """Calculate all positions for this word placement."""
        if not self.positions:
            self.positions = self._calculate_positions()

    def _calculate_positions(self) -> List[Position]:
        """Calculate all grid positions occupied by this word."""
        positions = []
        for i in range(len(self.word.value)):
            row = self.start_position.row + i * self.direction.row_delta
            col = self.start_position.col + i * self.direction.col_delta
            positions.append(Position(row, col))
        return positions

    def get_character_at(self, index: int) -> str:
        """Get the character at a specific index in the word."""
        return self.word.value[index]


@dataclass
class Puzzle:
    """Entity representing a complete word search puzzle."""
    grid_size: int
    words: List[Word]
    placements: List[WordPlacement] = field(default_factory=list)
    grid: List[List[str]] = field(default_factory=list)

    def __post_init__(self):
        """Initialize empty grid if not provided."""
        if not self.grid:
            self.grid = [['' for _ in range(self.grid_size)]
                        for _ in range(self.grid_size)]

    def is_valid_position(self, position: Position) -> bool:
        """Check if a position is within grid bounds."""
        return (0 <= position.row < self.grid_size and
                0 <= position.col < self.grid_size)

    def get_cell(self, position: Position) -> str:
        """Get the character at a specific position."""
        if not self.is_valid_position(position):
            raise ValueError(f"Position {position} is out of bounds")
        return self.grid[position.row][position.col]

    def set_cell(self, position: Position, character: str) -> None:
        """Set the character at a specific position."""
        if not self.is_valid_position(position):
            raise ValueError(f"Position {position} is out of bounds")
        self.grid[position.row][position.col] = character

    def add_placement(self, placement: WordPlacement) -> None:
        """Add a word placement to the puzzle."""
        for i, position in enumerate(placement.positions):
            character = placement.get_character_at(i)
            self.set_cell(position, character)
        self.placements.append(placement)

    def can_place_word(self, word: Word, start: Position, direction: Direction) -> bool:
        """Check if a word can be placed at the given position and direction."""
        for i, char in enumerate(word.value):
            row = start.row + i * direction.row_delta
            col = start.col + i * direction.col_delta
            position = Position(row, col)

            if not self.is_valid_position(position):
                return False

            existing_char = self.get_cell(position)
            if existing_char != '' and existing_char != char:
                return False

        return True

    def is_complete(self) -> bool:
        """Check if all words have been placed."""
        return len(self.placements) >= len(self.words)

    def reset(self) -> None:
        """Reset the puzzle to empty state."""
        self.grid = [['' for _ in range(self.grid_size)]
                    for _ in range(self.grid_size)]
        self.placements = []
