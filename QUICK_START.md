# Quick Start Guide

## For Users Who Just Want to Generate Puzzles

### Fastest Way (Original Version)
```bash
python3 multi_puzzle_word_search.py
```

This generates a puzzle with default settings immediately.

### Custom Puzzle
```bash
python3 multi_puzzle_word_search.py --size 12 --words PYTHON JAVA RUBY GOLANG
```

## For Developers Learning Clean Architecture

### Using Clean Architecture Version
```bash
python3 main.py --size 12 --words PYTHON JAVA RUBY GOLANG
```

**Same result, professional architecture!**

## Common Commands

```bash
# Default puzzle (9x9, Christmas theme)
python3 main.py

# Custom size and words
python3 main.py --size 15 --words APPLE BANANA ORANGE GRAPE

# Load words from file
python3 main.py --wordfile my_words.txt --size 20

# Full customization
python3 main.py \
  --size 20 \
  --wordfile words.txt \
  --output my_puzzle.html \
  --title "My Amazing Puzzle" \
  --count 15
```

## Available Options

| Option | Description | Default |
|--------|-------------|---------|
| `--size` | Grid size (5-30) | 9 |
| `--words` | Space-separated word list | Christmas words |
| `--wordfile` | Path to words file (one per line) | None |
| `--output` | Output HTML filename | interactive_word_search.html |
| `--title` | Puzzle title | Word Search Puzzle |
| `--count` | Number of puzzles to generate | 10 |

## Understanding the Output

The program creates an HTML file that contains:
- Multiple pre-generated puzzle variations
- Interactive click-and-drag word selection
- Automatic word highlighting when found
- Progress tracker
- Victory celebration
- "New Puzzle" button to load next variation

## Tips

1. **Grid Size**: Should be at least as large as your longest word
2. **Word Count**: 8-15 words work well for most grid sizes
3. **Puzzle Count**: 10-20 puzzles provide good variety
4. **Word File Format**: One word per line, plain text

## Examples

### Educational Puzzle
```bash
python3 main.py \
  --size 12 \
  --words ATOM PROTON NEUTRON ELECTRON NUCLEUS \
  --title "Chemistry Terms"
```

### Reading List
```bash
echo -e "PYTHON\nJAVA\nRUST\nGO\nRUBY" > languages.txt
python3 main.py --wordfile languages.txt --size 10
```

### Large Puzzle
```bash
python3 main.py --size 25 --wordfile big_wordlist.txt --count 20
```

## Troubleshooting

### Error: Word won't fit in grid
**Problem**: `Longest word 'EXAMPLE' (7 letters) won't fit in 5x5 grid`

**Solution**: Increase grid size
```bash
python3 main.py --size 10  # Use at least the length of longest word
```

### Error: File not found
**Problem**: `Error: File 'words.txt' not found`

**Solution**: Check file path
```bash
ls words.txt  # Verify file exists
python3 main.py --wordfile ./words.txt  # Use relative path
```

### Only generated X puzzles instead of Y
**Problem**: `Warning: Only generated 5 puzzles out of 10 requested`

**Solution**: Grid too small for words, increase size
```bash
python3 main.py --size 15  # Larger grid = easier placement
```

## For Developers

### Project Structure
```
.
├── main.py                          # Clean Architecture version
├── multi_puzzle_word_search.py      # Original/Clean Code version
├── word_puzzle/                     # Clean Architecture package
│   ├── domain/                      # Business logic
│   ├── application/                 # Use cases
│   ├── infrastructure/              # External interfaces
│   └── presentation/                # UI/Output
├── ARCHITECTURE.md                  # Architecture docs
├── COMPARISON.md                    # Version comparison
├── SUMMARY.md                       # Refactoring summary
└── README.md                        # Original README
```

### Running Tests
```bash
# Test with small puzzle (fast)
python3 main.py --size 8 --words HELLO WORLD --count 2

# Test validation
python3 main.py --size 5 --words TOOLONGWORD  # Should show error

# Test file loading
echo "TEST" > test.txt
python3 main.py --wordfile test.txt --size 10
rm test.txt
```

### Programmatic Usage
```python
from word_puzzle.domain import Puzzle, Word
from word_puzzle.application import PuzzleGenerationStrategy

# Create puzzle
words = [Word("PYTHON"), Word("CODE")]
puzzle = Puzzle(grid_size=10, words=words)

# Generate
strategy = PuzzleGenerationStrategy()
if strategy.generate(puzzle):
    print("Success!")
    for row in puzzle.grid:
        print(' '.join(row))
```

## Get Help

```bash
python3 main.py --help
```

## Learn More

- **Basic Usage**: See `README.md`
- **Architecture**: See `ARCHITECTURE.md`
- **Summary**: See `SUMMARY.md`
