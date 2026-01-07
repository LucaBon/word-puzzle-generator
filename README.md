# Multi-Puzzle Word Search Generator

A Python-based interactive word search puzzle generator that creates beautiful, fully-featured HTML puzzles with multiple pre-generated variations. Perfect for creating educational materials, entertainment, or themed puzzles.

## Features

- **Multiple Puzzles**: Generate multiple unique puzzle variations in a single HTML file
- **Interactive Gameplay**: Click and drag to select words with smart directional locking
- **Responsive Design**: Automatically adapts to different grid sizes (5x5 to 30x30)
- **Configurable**: Command-line interface for easy customization
- **Beautiful UI**: Modern gradient design with smooth animations
- **Progress Tracking**: Visual feedback showing found words and completion status
- **Touch Support**: Works on mobile devices and tablets
- **Adaptive Layout**: Word list automatically adjusts based on quantity (single/multi-column)

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Installation

Simply download the `multi_puzzle_word_search.py` file. No installation required!

## Usage

### Basic Usage (Default Settings)

```bash
python multi_puzzle_word_search.py
```

This generates a puzzle with:
- 9x9 grid
- Default Christmas-themed words (Italian)
- 10 unique puzzle variations
- Output file: `interactive_word_search.html`

### Custom Grid Size

```bash
python multi_puzzle_word_search.py --size 15
```

### Custom Words (Inline)

```bash
python multi_puzzle_word_search.py --size 12 --words PYTHON CODE SEARCH PUZZLE WORD FIND GAME
```

### Load Words from File

Create a text file with one word per line:

```text
PYTHON
JAVASCRIPT
HTML
CSS
REACT
DJANGO
```

Then generate the puzzle:

```bash
python multi_puzzle_word_search.py --wordfile words.txt --size 15
```

### Full Customization

```bash
python multi_puzzle_word_search.py \
  --size 20 \
  --wordfile programming_words.txt \
  --output programming_puzzle.html \
  --title "Programming Word Search" \
  --count 20
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

### Example 1: Educational Puzzle

```bash
python multi_puzzle_word_search.py \
  --size 12 \
  --words ATOM PROTON NEUTRON ELECTRON NUCLEUS MOLECULE \
  --title "Chemistry Word Search" \
  --count 5
```

### Example 2: Large Puzzle with Many Words

```bash
python multi_puzzle_word_search.py \
  --size 25 \
  --wordfile countries.txt \
  --title "Countries of the World" \
  --count 15
```

### Example 3: Compact Puzzle

```bash
python multi_puzzle_word_search.py \
  --size 8 \
  --words CAT DOG BIRD FISH \
  --title "Pets"
```

## Adaptive Features

### Grid Size Adaptations

The puzzle automatically adjusts cell size based on grid dimensions:

- **Size ≤ 10**: 50px cells, 22px font (comfortable)
- **Size 11-15**: 45px cells, 20px font (standard)
- **Size 16-20**: 35px cells, 16px font (compact)
- **Size > 20**: 28px cells, 14px font (very compact)

### Word List Adaptations

The word list layout automatically adjusts based on quantity:

- **≤ 10 words**: Single column, large items
- **11-20 words**: Single column, medium items
- **21-30 words**: Two columns, smaller items
- **> 30 words**: Two columns, compact items

On mobile devices, the word list always displays in a single column regardless of word count.

## Gameplay Features

### How to Play

1. **Select Words**: Click and drag across letters to select a word
2. **Directional Locking**: After selecting two cells, the selection locks to that direction (horizontal, vertical, or diagonal)
3. **Find All Words**: Words can be placed in any of 8 directions
4. **New Puzzle**: Click "New Puzzle" button to load a fresh variation
5. **Victory**: Complete all words to see the victory message

### Visual Feedback

- **Hover Effect**: Cells highlight when hovering
- **Selection**: Blue highlight while selecting
- **Found Words**: Green highlight when word is found
- **Crossed Off**: Found words are struck through in the word list
- **Progress Tracker**: Shows X/Y words found

## Tips for Best Results

1. **Grid Size**: Choose a grid size appropriate for your words
   - Minimum size = length of longest word
   - Recommended: Add 3-5 extra cells for better word placement

2. **Word Count**:
   - 8-15 words work well for most grid sizes
   - Larger grids (20+) can accommodate 20-30 words

3. **Word Length Mix**: Include a variety of word lengths for better puzzle layout

4. **Puzzle Count**: Generate 10-20 puzzles for good variety without excessive generation time

## Validation

The script includes automatic validation:

- Checks if words fit in the grid
- Validates grid size (5-30)
- Ensures at least one word is provided
- Verifies file existence when using `--wordfile`
- Provides helpful error messages

## Output

The generator creates a single HTML file containing:

- All puzzle variations embedded as JSON data
- Complete CSS styling (no external dependencies)
- JavaScript for interactivity
- Touch and mouse support
- Responsive layout

The HTML file can be:
- Opened directly in any modern web browser
- Shared via email or cloud storage
- Hosted on a web server
- Printed (though interactive features won't work)

## Browser Compatibility

- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera
- Mobile browsers (iOS Safari, Chrome Mobile)

Requires JavaScript enabled for interactivity.

## Troubleshooting

### Problem: Only 1 puzzle generated instead of 10

**Solution**: The grid might be too small for the words. Try:
```bash
python multi_puzzle_word_search.py --size 12
```

### Problem: Word doesn't fit in grid

**Error**: `Longest word 'EXAMPLE' (7 letters) won't fit in 5x5 grid`

**Solution**: Increase grid size:
```bash
python multi_puzzle_word_search.py --size 10
```

### Problem: Words not rendering on mobile

**Solution**: The layout is responsive. Try landscape orientation for larger grids.

## Technical Details

### Word Placement Algorithm

- Places longer words first for better space utilization
- Balances word directions (horizontal, vertical, diagonal)
- Allows word intersections at matching letters
- Attempts multiple positions until successful placement
- Fills empty cells with random letters

### Performance

- Typical generation time: 1-5 seconds for 10 puzzles
- Handles up to 30x30 grids efficiently
- Scales well with word count (tested up to 50 words)

## License

This project is provided as-is for educational and personal use.

## Contributing

Feel free to modify and enhance the code for your needs. Some ideas:

- Add more color themes
- Implement hint system
- Add timer/scoring
- Support for multiple languages
- PDF export option
- Difficulty levels

## Changelog

### Version 1.0
- Initial release with basic functionality
- Command-line interface
- Multiple puzzle generation
- Responsive design
- Adaptive grid and word list sizing
