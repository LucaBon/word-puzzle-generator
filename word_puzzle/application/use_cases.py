"""
Application Use Cases - Application-specific business rules
Each use case represents a single user action or system operation
"""
from typing import List, Optional
from dataclasses import dataclass
from ..domain import Puzzle, Word, GridSize
from .interfaces import (
    IWordRepository, IPuzzleRepository,
    IPuzzlePresenter, IConfigValidator
)
from .services import PuzzleGenerationStrategy


@dataclass
class GeneratePuzzleRequest:
    """Input data for puzzle generation use case."""
    grid_size: int
    words: Optional[List[str]] = None
    word_file: Optional[str] = None
    puzzle_count: int = 10
    output_file: str = 'interactive_word_search.html'
    title: str = 'Word Search Puzzle'


@dataclass
class GeneratePuzzleResponse:
    """Output data from puzzle generation use case."""
    success: bool
    puzzles: List[Puzzle]
    message: str
    puzzles_generated: int


class GeneratePuzzleUseCase:
    """
    Use Case: Generate word search puzzles
    Orchestrates the puzzle generation process
    """

    def __init__(
        self,
        word_repository: IWordRepository,
        puzzle_repository: IPuzzleRepository,
        presenter: IPuzzlePresenter,
        validator: IConfigValidator,
        generation_strategy: Optional[PuzzleGenerationStrategy] = None
    ):
        self.word_repository = word_repository
        self.puzzle_repository = puzzle_repository
        self.presenter = presenter
        self.validator = validator
        self.generation_strategy = generation_strategy or PuzzleGenerationStrategy()

    def execute(self, request: GeneratePuzzleRequest) -> GeneratePuzzleResponse:
        """Execute the puzzle generation use case."""
        try:
            # 1. Load words
            words = self._load_words(request)

            # 2. Validate configuration
            self._validate_configuration(request.grid_size, words)

            # 3. Generate puzzles
            puzzles = self._generate_puzzles(
                request.grid_size,
                words,
                request.puzzle_count
            )

            # 4. Save puzzles
            self._save_puzzles(puzzles, request)

            return GeneratePuzzleResponse(
                success=True,
                puzzles=puzzles,
                message=f"Successfully generated {len(puzzles)} puzzles",
                puzzles_generated=len(puzzles)
            )

        except Exception as e:
            return GeneratePuzzleResponse(
                success=False,
                puzzles=[],
                message=f"Failed to generate puzzles: {str(e)}",
                puzzles_generated=0
            )

    def _load_words(self, request: GeneratePuzzleRequest) -> List[Word]:
        """Load words from specified source."""
        if request.word_file:
            return self.word_repository.load_from_file(request.word_file)
        elif request.words:
            return [Word(w) for w in request.words]
        else:
            return self.word_repository.get_default_words()

    def _validate_configuration(self, grid_size: int, words: List[Word]) -> None:
        """Validate puzzle configuration."""
        self.validator.validate_grid_size(grid_size)
        self.validator.validate_words(words, grid_size)

    def _generate_puzzles(
        self,
        grid_size: int,
        words: List[Word],
        count: int
    ) -> List[Puzzle]:
        """Generate multiple puzzles."""
        puzzles = []
        max_attempts = count * 10

        for attempt in range(max_attempts):
            if len(puzzles) >= count:
                break

            puzzle = Puzzle(grid_size=grid_size, words=words)
            if self.generation_strategy.generate(puzzle):
                puzzles.append(puzzle)
                print(f"  Generated puzzle {len(puzzles)}/{count}")

        if len(puzzles) < count:
            print(f"\n⚠ Warning: Only generated {len(puzzles)} puzzles out of {count} requested.")
            print("  Try using a larger grid size or fewer/shorter words.")

        return puzzles

    def _save_puzzles(self, puzzles: List[Puzzle], request: GeneratePuzzleRequest) -> None:
        """Save puzzles using repository and presenter."""
        metadata = {
            'title': request.title,
            'output_file': request.output_file
        }

        # Present puzzles in desired format
        presented_data = self.presenter.present(puzzles, metadata)

        # Save through repository
        if puzzles:
            self.puzzle_repository.save(presented_data, request.output_file)


@dataclass
class ValidateConfigRequest:
    """Input data for configuration validation use case."""
    grid_size: int
    words: List[str]


@dataclass
class ValidateConfigResponse:
    """Output data from configuration validation."""
    valid: bool
    errors: List[str]


class ValidateConfigUseCase:
    """Use Case: Validate puzzle configuration."""

    def __init__(self, validator: IConfigValidator):
        self.validator = validator

    def execute(self, request: ValidateConfigRequest) -> ValidateConfigResponse:
        """Execute the configuration validation use case."""
        errors = []

        try:
            self.validator.validate_grid_size(request.grid_size)
        except Exception as e:
            errors.append(str(e))

        try:
            words = [Word(w) for w in request.words]
            self.validator.validate_words(words, request.grid_size)
        except Exception as e:
            errors.append(str(e))

        return ValidateConfigResponse(
            valid=len(errors) == 0,
            errors=errors
        )
