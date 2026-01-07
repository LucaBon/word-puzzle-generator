#!/usr/bin/env python3
"""
Main entry point for the Word Puzzle Generator
This file wires together all the dependencies (Dependency Injection Container)
"""
import sys
from word_puzzle.application import (
    GeneratePuzzleUseCase,
    PuzzleGenerationStrategy
)
from word_puzzle.infrastructure import (
    FileWordRepository,
    HTMLFileRepository,
    PuzzleConfigValidator
)
from word_puzzle.presentation import (
    HTMLPuzzlePresenter,
    CLIController
)


def create_app() -> CLIController:
    """
    Dependency Injection Container
    Creates and wires all dependencies following the Dependency Inversion Principle

    Dependencies flow from outer layers to inner layers:
    Presentation -> Application -> Domain
                 -> Infrastructure -> Application
    """
    # Infrastructure Layer (outer) - Concrete implementations
    word_repository = FileWordRepository()
    puzzle_repository = HTMLFileRepository()
    validator = PuzzleConfigValidator()

    # Presentation Layer (outer) - UI components
    presenter = HTMLPuzzlePresenter()

    # Application Layer (middle) - Business logic coordination
    generation_strategy = PuzzleGenerationStrategy(max_attempts=1000)
    use_case = GeneratePuzzleUseCase(
        word_repository=word_repository,
        puzzle_repository=puzzle_repository,
        presenter=presenter,
        validator=validator,
        generation_strategy=generation_strategy
    )

    # Presentation Controller - Entry point
    controller = CLIController(use_case)

    return controller


def main():
    """Application entry point."""
    app = create_app()
    exit_code = app.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
