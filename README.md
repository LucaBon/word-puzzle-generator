# Word Search Puzzle Generator

A Python-based word search puzzle generator. Creates beautiful, interactive HTML puzzles with multiple pre-generated variations.

## Features

- **Multiple Puzzles**: Generate multiple unique puzzle variations in a single HTML file
- **Interactive Gameplay**: Click and drag to select words with smart directional locking
- **Responsive Design**: Automatically adapts to different grid sizes (5x5 to 30x30)
- **Configurable**: Command-line interface for easy customization
- **Beautiful UI**: Modern gradient design with smooth animations
- **Progress Tracking**: Visual feedback showing found words and completion status
- **Touch Support**: Works on mobile devices and tablets
- **Highly Testable**: Interface-based design allows easy testing and mocking
- **Extensible**: Easy to add new output formats, UIs, or storage mechanisms

## Quick Start

### Installation

```bash
# No installation required! Just Python 3.6+
git clone <repository>
cd WordPuzzleGenerator
```

### Basic Usage

```bash
# Generate default puzzle (9x9 grid, Christmas theme)
python3 main.py

# Custom puzzle
python3 main.py --size 12 --words PYTHON CODE PUZZLE

# Load words from file
python3 main.py --wordfile words.txt --size 15
```

## Architecture

This project follows **Clean Architecture** principles:

```
┌─────────────────────────────────────┐
│   Presentation (CLI, HTML)          │
├─────────────────────────────────────┤
│   Infrastructure (Files, Validators)│
├─────────────────────────────────────┤
│   Application (Use Cases)           │
├─────────────────────────────────────┤
│   Domain (Business Logic)           │
└─────────────────────────────────────┘
```

### Project Structure

```
word_puzzle/
├── domain/              # Core business logic
│   ├── entities.py      # Puzzle, WordPlacement
│   └── value_objects.py # Word, Position, Direction
├── application/         # Use cases
│   ├── interfaces.py    # Abstract interfaces
│   ├── services.py      # Business services
│   └── use_cases.py     # Use case implementations
├── infrastructure/      # External implementations
│   ├── repositories.py  # File storage
│   └── validators.py    # Validation
└── presentation/        # UI and output
    ├── cli_controller.py  # CLI interface
    └── html_presenter.py  # HTML generation

main.py                  # Entry point (DI container)
```

## Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--size` | Grid size (5-30) | 9 |
| `--words` | Space-separated list of words | Christmas words |
| `--wordfile` | Path to text file with words (one per line) | None |
| `--output` | Output HTML filename | `interactive_word_search.html` |
| `--title` | Puzzle title | "Word Search Puzzle" |
| `--count` | Number of puzzles to generate | 10 |
| `--help` | Show help message | - |

## Examples

### Educational Puzzle

```bash
python3 main.py \
  --size 12 \
  --words ATOM PROTON NEUTRON ELECTRON NUCLEUS MOLECULE \
  --title "Chemistry Word Search" \
  --count 5
```

### Words from File

```bash
# Create a words file
cat > languages.txt << EOF
PYTHON
JAVASCRIPT
JAVA
GOLANG
RUST
EOF

# Generate puzzle
python3 main.py --wordfile languages.txt --size 15
```

### Large Puzzle

```bash
python3 main.py \
  --size 25 \
  --wordfile countries.txt \
  --title "Countries of the World" \
  --count 20
```

## Programmatic Usage

```python
from word_puzzle.domain import Puzzle, Word
from word_puzzle.application import PuzzleGenerationStrategy

# Create puzzle
words = [Word("PYTHON"), Word("CODE"), Word("CLEAN")]
puzzle = Puzzle(grid_size=10, words=words)

# Generate
strategy = PuzzleGenerationStrategy()
if strategy.generate(puzzle):
    print("Success!")
    for row in puzzle.grid:
        print(' '.join(row))
```

## Design Patterns Used

- **Repository Pattern**: Abstract data access
- **Dependency Injection**: Constructor injection
- **Use Case Pattern**: Each action is a use case
- **Strategy Pattern**: Pluggable generation algorithms
- **Presenter Pattern**: Separate logic from presentation
- **Value Object Pattern**: Immutable, self-validating objects

## Benefits of Clean Architecture

### Testability

```python
# Test domain logic independently
def test_puzzle_placement():
    puzzle = Puzzle(grid_size=5, words=[Word("HELLO")])
    assert puzzle.can_place_word(
        Word("HELLO"),
        Position(0, 0),
        Directions.HORIZONTAL_RIGHT
    )
```

### Flexibility

Want to add PDF export? Just implement the interface:

```python
class PDFPresenter(IPuzzlePresenter):
    def present(self, puzzles, metadata):
        return generate_pdf(puzzles)
```

### Maintainability

- Clear separation of concerns
- Each layer has a single responsibility
- Easy to locate and modify code
- Changes in one layer don't affect others

## Documentation

- **[QUICK_START.md](QUICK_START.md)** - Get started immediately
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Detailed architecture documentation
- **[COMPARISON.md](COMPARISON.md)** - Architecture evolution comparison
- **[SUMMARY.md](SUMMARY.md)** - Complete refactoring summary

## Adaptive Features

### Grid Size Adaptations

- **≤ 10**: 50px cells, 22px font (comfortable)
- **11-15**: 45px cells, 20px font (standard)
- **16-20**: 35px cells, 16px font (compact)
- **> 20**: 28px cells, 14px font (very compact)

### Word List Adaptations

- **≤ 10 words**: Single column, large items
- **11-20 words**: Single column, medium items
- **21-30 words**: Two columns, smaller items
- **> 30 words**: Two columns, compact items

## How to Play

1. **Select Words**: Click and drag across letters
2. **Directional Locking**: Selection locks to direction after two cells
3. **Find All Words**: Words can be in any of 8 directions
4. **New Puzzle**: Click button to load next variation
5. **Victory**: Complete all words for celebration

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Browser Compatibility

- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera
- Mobile browsers (iOS Safari, Chrome Mobile)

Requires JavaScript enabled for interactivity.

## Troubleshooting

### Error: Word won't fit in grid

```bash
# Increase grid size
python3 main.py --size 15
```

### Error: Only generated X puzzles

```bash
# Grid too small, increase size
python3 main.py --size 20
```

### Error: File not found

```bash
# Check file path
ls words.txt
python3 main.py --wordfile ./words.txt
```

## Future Enhancements

Easy to add with current architecture:

- ✅ PDF/PNG export (implement `IPuzzlePresenter`)
- ✅ Web interface (create `WebController`)
- ✅ Database storage (implement `IPuzzleRepository`)
- ✅ REST API (create `APIController`)
- ✅ Different algorithms (implement `Strategy`)
- ✅ Difficulty levels (add to domain)
- ✅ Puzzle solver (new use case)
- ✅ Hints system (domain service)

## Performance

- Typical generation time: 1-5 seconds for 10 puzzles
- Handles up to 30x30 grids efficiently
- Scales well with word count (tested up to 50 words)

## License

This project is provided as-is for educational and personal use.

## Learn More

- [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) by Robert C. Martin
- [Domain-Driven Design](https://www.domainlanguage.com/ddd/) by Eric Evans
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)

## Version

**2.0.0** - Refactored Architecture Implementation

### Changelog

#### Version 2.0.0 (Refactored Architecture)
- Complete refactoring
- Separation into domain, application, infrastructure, and presentation layers
- Dependency inversion and injection
- Interface-based design for flexibility
- Enhanced testability and maintainability

#### Version 1.0.0
- Initial release with basic functionality
- Command-line interface
- Multiple puzzle generation
- Responsive HTML output
