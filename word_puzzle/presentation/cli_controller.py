"""
Presentation Layer - CLI Controller
Handles command-line interface and user interactions
"""
import argparse
from typing import Optional
from ..application import GeneratePuzzleUseCase, GeneratePuzzleRequest


class CLIController:
    """Controller for command-line interface."""

    DEFAULT_GRID_SIZE = 9
    DEFAULT_PUZZLE_COUNT = 10

    def __init__(self, use_case: GeneratePuzzleUseCase):
        self.use_case = use_case

    def run(self, args: Optional[list] = None) -> int:
        """Run the CLI application."""
        parser = self._create_argument_parser()
        parsed_args = parser.parse_args(args)

        # Create request from CLI arguments
        request = GeneratePuzzleRequest(
            grid_size=parsed_args.size,
            words=parsed_args.words,
            word_file=parsed_args.wordfile,
            puzzle_count=parsed_args.count,
            output_file=parsed_args.output,
            title=parsed_args.title
        )

        # Print generation info
        self._print_generation_info(request)

        # Execute use case
        response = self.use_case.execute(request)

        # Print results
        if response.success:
            self._print_success_info(response)
            return 0
        else:
            print(f"\n✗ Error: {response.message}")
            return 1

    def _create_argument_parser(self) -> argparse.ArgumentParser:
        """Create and configure argument parser."""
        parser = argparse.ArgumentParser(
            description='Generate interactive word search puzzles',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s
  %(prog)s --size 12
  %(prog)s --size 10 --words PYTHON CODE SEARCH PUZZLE WORD
  %(prog)s --wordfile words.txt --size 15
  %(prog)s --output my_puzzle.html --title "My Puzzle" --count 20
            """
        )

        parser.add_argument(
            '--size', type=int, default=self.DEFAULT_GRID_SIZE,
            help=f'Grid size (default: {self.DEFAULT_GRID_SIZE})'
        )
        parser.add_argument(
            '--words', nargs='+',
            help='List of words to include in the puzzle (space-separated)'
        )
        parser.add_argument(
            '--wordfile', type=str,
            help='Path to a text file containing words (one per line)'
        )
        parser.add_argument(
            '--output', type=str, default='interactive_word_search.html',
            help='Output HTML filename (default: interactive_word_search.html)'
        )
        parser.add_argument(
            '--title', type=str, default='Word Search Puzzle',
            help='Puzzle title (default: Word Search Puzzle)'
        )
        parser.add_argument(
            '--count', type=int, default=self.DEFAULT_PUZZLE_COUNT,
            help=f'Number of puzzles to generate (default: {self.DEFAULT_PUZZLE_COUNT})'
        )

        return parser

    def _print_generation_info(self, request: GeneratePuzzleRequest) -> None:
        """Print information about puzzle generation."""
        word_source = "file" if request.word_file else "custom" if request.words else "default"
        word_count = len(request.words) if request.words else "default"

        print(f"\nGenerating multiple {request.grid_size}x{request.grid_size} interactive word search puzzles...")
        if isinstance(word_count, int):
            print(f"Words to place: {word_count}")
        print(f"Output file: {request.output_file}")
        print(f"Puzzle title: {request.title}")
        print(f"Number of puzzles: {request.puzzle_count}")

    def _print_success_info(self, response) -> None:
        """Print success information after generation."""
        print(f"✓ Generated {response.puzzles_generated} unique puzzles!")
        print("\n✓ Interactive puzzle generated successfully!")
        print("\n📝 Features:")
        print(f"   • {response.puzzles_generated} different unique puzzles pre-generated")
        print("   • Click 'New Puzzle' button to get a fresh puzzle")
        print("   • Smart directional locking for easy diagonal selection")
        print("   • Found words automatically highlight in green")
        print("   • Words are crossed off the list when found")
        print("   • Progress tracker shows how many words found")
        print("   • Victory celebration when all words are found")
