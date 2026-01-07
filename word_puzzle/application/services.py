"""
Application Services - Domain services and puzzle generation strategies
These contain application-specific business logic
"""
import random
from typing import List, Dict
from ..domain import (
    Puzzle, WordPlacement, Position, Direction, Word,
    Directions, DirectionType
)


class DirectionBalancer:
    """Service to balance word placement across different directions."""

    def __init__(self, total_words: int):
        self.total_words = total_words
        self.counts = {
            DirectionType.HORIZONTAL: 0,
            DirectionType.VERTICAL: 0,
            DirectionType.DIAGONAL: 0
        }

    def increment(self, direction: Direction) -> None:
        """Increment count for a direction."""
        if direction.is_horizontal():
            self.counts[DirectionType.HORIZONTAL] += 1
        elif direction.is_vertical():
            self.counts[DirectionType.VERTICAL] += 1
        else:
            self.counts[DirectionType.DIAGONAL] += 1

    def get_priority_directions(self, word_index: int) -> List[Direction]:
        """Get directions in priority order for balanced placement."""
        target_per_category = self.total_words // 3

        horizontal = Directions.horizontal()
        vertical = Directions.vertical()
        diagonal = Directions.diagonal()

        # Prioritize underrepresented directions
        if self.counts[DirectionType.DIAGONAL] < target_per_category:
            return diagonal + horizontal + vertical
        elif self.counts[DirectionType.HORIZONTAL] < target_per_category:
            return horizontal + diagonal + vertical
        elif self.counts[DirectionType.VERTICAL] < target_per_category:
            return vertical + diagonal + horizontal
        else:
            # Round-robin when balanced
            all_directions = [horizontal, vertical, diagonal]
            group_idx = word_index % len(all_directions)
            selected = all_directions[group_idx]
            others = [d for i, group in enumerate(all_directions)
                     if i != group_idx for d in group]
            return selected + others

    def has_sufficient_diagonal_coverage(self, min_percentage: float = 0.2) -> bool:
        """Check if diagonal coverage meets minimum threshold."""
        return self.counts[DirectionType.DIAGONAL] >= self.total_words * min_percentage


class WordPlacementService:
    """Service for placing words in the puzzle grid."""

    def __init__(self, puzzle: Puzzle):
        self.puzzle = puzzle

    def try_place_word(self, word: Word, directions: List[Direction]) -> bool:
        """Try to place a word using given directions."""
        random.shuffle(directions)

        for direction in directions:
            positions = self._get_all_positions()
            random.shuffle(positions)

            for position in positions:
                if self.puzzle.can_place_word(word, position, direction):
                    placement = WordPlacement(word, position, direction)
                    self.puzzle.add_placement(placement)
                    return True

        return False

    def _get_all_positions(self) -> List[Position]:
        """Get all possible grid positions."""
        return [Position(r, c)
                for r in range(self.puzzle.grid_size)
                for c in range(self.puzzle.grid_size)]

    def fill_empty_cells(self) -> None:
        """Fill all empty cells with random letters."""
        import string
        for row in range(self.puzzle.grid_size):
            for col in range(self.puzzle.grid_size):
                position = Position(row, col)
                if self.puzzle.get_cell(position) == '':
                    self.puzzle.set_cell(position, random.choice(string.ascii_uppercase))


class PuzzleGenerationStrategy:
    """Strategy for generating puzzles with balanced word placement."""

    def __init__(self, max_attempts: int = 1000):
        self.max_attempts = max_attempts

    def generate(self, puzzle: Puzzle) -> bool:
        """Generate a complete puzzle with balanced word placement."""
        sorted_words = sorted(puzzle.words, key=len, reverse=True)

        for _ in range(self.max_attempts):
            puzzle.reset()
            words_to_place = sorted_words.copy()
            random.shuffle(words_to_place)

            if self._attempt_placement(puzzle, words_to_place):
                placement_service = WordPlacementService(puzzle)
                placement_service.fill_empty_cells()
                return True

        return False

    def _attempt_placement(self, puzzle: Puzzle, words: List[Word]) -> bool:
        """Attempt to place all words with balanced directions."""
        balancer = DirectionBalancer(len(words))
        placement_service = WordPlacementService(puzzle)

        for i, word in enumerate(words):
            priority_directions = balancer.get_priority_directions(i)

            if placement_service.try_place_word(word, priority_directions):
                last_placement = puzzle.placements[-1]
                balancer.increment(last_placement.direction)
            else:
                return False

        return balancer.has_sufficient_diagonal_coverage()
