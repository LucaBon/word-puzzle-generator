import random
import string
from typing import List, Tuple, Optional
import json
import argparse
import sys

class MultiPuzzleWordSearchGenerator:
    """
    A class to generate interactive word search puzzles with client-side puzzle generation.
    """
    
    # Direction vectors: (row_delta, col_delta, direction_name)
    DIRECTIONS = [
        (0, 1, 'horizontal_right'),      # Left to right
        (0, -1, 'horizontal_left'),      # Right to left
        (1, 0, 'vertical_down'),         # Top to bottom
        (-1, 0, 'vertical_up'),          # Bottom to top
        (1, 1, 'diagonal_down_right'),   # Diagonal down-right
        (1, -1, 'diagonal_down_left'),   # Diagonal down-left
        (-1, 1, 'diagonal_up_right'),    # Diagonal up-right
        (-1, -1, 'diagonal_up_left')     # Diagonal up-left
    ]
    
    def __init__(self, size: int, words: List[str]):
        """
        Initialize the word search generator.
        """
        self.size = size
        self.words = [word.upper() for word in words]
        self.grid = [['' for _ in range(size)] for _ in range(size)]
        self.placed_words = []
        
    def can_place_word(self, word: str, row: int, col: int, 
                       row_delta: int, col_delta: int) -> bool:
        """
        Check if a word can be placed at the given position and direction.
        """
        end_row = row + row_delta * (len(word) - 1)
        end_col = col + col_delta * (len(word) - 1)
        
        if not (0 <= end_row < self.size and 0 <= end_col < self.size):
            return False
        
        for i, char in enumerate(word):
            current_row = row + i * row_delta
            current_col = col + i * col_delta
            cell = self.grid[current_row][current_col]
            
            if cell != '' and cell != char:
                return False
        
        return True
    
    def place_word(self, word: str, row: int, col: int, 
                   row_delta: int, col_delta: int, direction_name: str) -> None:
        """
        Place a word in the grid at the specified position and direction.
        """
        cells = []
        for i, char in enumerate(word):
            current_row = row + i * row_delta
            current_col = col + i * col_delta
            self.grid[current_row][current_col] = char
            cells.append([current_row, current_col])
        
        self.placed_words.append({
            'word': word,
            'start': (row, col),
            'direction': direction_name,
            'cells': cells
        })
    
    def try_place_word(self, word: str, direction_indices: List[int]) -> bool:
        """
        Try to place a word using the specified directions.
        """
        random.shuffle(direction_indices)
        
        for dir_idx in direction_indices:
            row_delta, col_delta, direction_name = self.DIRECTIONS[dir_idx]
            
            positions = [(r, c) for r in range(self.size) for c in range(self.size)]
            random.shuffle(positions)
            
            for row, col in positions:
                if self.can_place_word(word, row, col, row_delta, col_delta):
                    self.place_word(word, row, col, row_delta, col_delta, direction_name)
                    return True
        
        return False
    
    def generate(self, max_attempts: int = 1000) -> bool:
        """
        Generate the word search puzzle with balanced word placement.
        """
        sorted_words = sorted(self.words, key=len, reverse=True)
        
        horizontal = [0, 1]
        vertical = [2, 3]
        diagonal = [4, 5, 6, 7]
        
        direction_groups = [horizontal, vertical, diagonal]
        
        for attempt in range(max_attempts):
            self.grid = [['' for _ in range(self.size)] for _ in range(self.size)]
            self.placed_words = []
            
            words_to_place = sorted_words.copy()
            random.shuffle(words_to_place)
            
            success = True
            direction_counts = {'horizontal': 0, 'vertical': 0, 'diagonal': 0}
            
            for i, word in enumerate(words_to_place):
                if direction_counts['diagonal'] < len(words_to_place) // 3:
                    priority_groups = [diagonal, horizontal, vertical]
                elif direction_counts['horizontal'] < len(words_to_place) // 3:
                    priority_groups = [horizontal, diagonal, vertical]
                elif direction_counts['vertical'] < len(words_to_place) // 3:
                    priority_groups = [vertical, diagonal, horizontal]
                else:
                    group_idx = i % len(direction_groups)
                    priority_groups = [direction_groups[group_idx]] + [g for j, g in enumerate(direction_groups) if j != group_idx]
                
                placed = False
                for group in priority_groups:
                    if self.try_place_word(word, group.copy()):
                        last_placement = self.placed_words[-1]['direction']
                        if 'horizontal' in last_placement:
                            direction_counts['horizontal'] += 1
                        elif 'vertical' in last_placement:
                            direction_counts['vertical'] += 1
                        else:
                            direction_counts['diagonal'] += 1
                        placed = True
                        break
                
                if not placed:
                    success = False
                    break
            
            if success:
                if direction_counts['diagonal'] >= len(words_to_place) * 0.2:
                    self.fill_empty_cells()
                    return True
        
        return False
    
    def fill_empty_cells(self) -> None:
        """
        Fill all empty cells with random letters.
        """
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == '':
                    self.grid[row][col] = random.choice(string.ascii_uppercase)
    
    def generate_multiple_puzzles(self, count: int = 5) -> List[dict]:
        """
        Generate multiple different puzzles.
        """
        puzzles = []
        attempts = 0
        max_total_attempts = count * 10  # Allow up to 10 attempts per puzzle

        while len(puzzles) < count and attempts < max_total_attempts:
            attempts += 1
            if self.generate():
                word_data = {}
                for placement in self.placed_words:
                    word_data[placement['word']] = placement['cells']

                puzzles.append({
                    'grid': [[self.grid[row][col] for col in range(self.size)] for row in range(self.size)],
                    'words': word_data
                })
                print(f"  Generated puzzle {len(puzzles)}/{count}")

        if len(puzzles) < count:
            print(f"\n⚠ Warning: Only generated {len(puzzles)} puzzles out of {count} requested.")
            print("  Try using a larger grid size or fewer/shorter words.")

        return puzzles
    
    def export_multi_puzzle_html(self, filename: str = "word_search.html", 
                                  title: str = "Word Search Puzzle",
                                  puzzle_count: int = 10) -> None:
        """
        Export multiple puzzles to an interactive HTML file.
        """
        puzzles = self.generate_multiple_puzzles(puzzle_count)
        
        # Calculate responsive cell size based on grid size
        # For grids > 15, make cells smaller to fit on screen
        if self.size <= 10:
            cell_size = 50
            font_size = 22
            gap = 3
            border_radius = 8
        elif self.size <= 15:
            cell_size = 45
            font_size = 20
            gap = 3
            border_radius = 6
        elif self.size <= 20:
            cell_size = 35
            font_size = 16
            gap = 2
            border_radius = 5
        else:  # > 20
            cell_size = 28
            font_size = 14
            gap = 2
            border_radius = 4

        # Calculate word list styling based on number of words
        word_count = len(self.words)
        if word_count <= 10:
            word_item_padding = "15px 20px"
            word_item_font_size = "1.2em"
            word_gap = "12px"
            words_section_width = "300px"
            words_list_columns = "1"
        elif word_count <= 20:
            word_item_padding = "12px 16px"
            word_item_font_size = "1.1em"
            word_gap = "10px"
            words_section_width = "320px"
            words_list_columns = "1"
        elif word_count <= 30:
            word_item_padding = "10px 14px"
            word_item_font_size = "1em"
            word_gap = "8px"
            words_section_width = "380px"
            words_list_columns = "2"
        else:  # > 30
            word_item_padding = "8px 12px"
            word_item_font_size = "0.95em"
            word_gap = "6px"
            words_section_width = "450px"
            words_list_columns = "2"

        # Calculate max width for container based on grid size
        grid_width = self.size * cell_size + (self.size - 1) * gap + 40  # +40 for padding
        words_width = int(words_section_width.replace('px', ''))
        container_max_width = max(1200, grid_width + words_width + 100)  # +100 for gap and margins

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        :root {{
            --cell-size: {cell_size}px;
            --font-size: {font_size}px;
            --grid-gap: {gap}px;
            --border-radius: {border_radius}px;
            --word-item-padding: {word_item_padding};
            --word-item-font-size: {word_item_font_size};
            --word-gap: {word_gap};
            --words-section-width: {words_section_width};
            --words-list-columns: {words_list_columns};
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow-x: auto;
        }}

        .container {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: {container_max_width}px;
            width: 100%;
        }}

        h1 {{
            text-align: center;
            color: #333;
            margin-bottom: 10px;
            font-size: clamp(1.5em, 3vw, 2.5em);
        }}

        .subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: clamp(0.9em, 2vw, 1.1em);
        }}

        .game-container {{
            display: flex;
            gap: 40px;
            justify-content: center;
            flex-wrap: wrap;
        }}

        .grid-section {{
            flex: 1;
            min-width: min(400px, 100%);
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .grid-container {{
            display: inline-block;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            user-select: none;
            max-width: 100%;
            overflow: auto;
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat({self.size}, var(--cell-size));
            gap: var(--grid-gap);
        }}

        .cell {{
            width: var(--cell-size);
            height: var(--cell-size);
            display: flex;
            align-items: center;
            justify-content: center;
            background: white;
            border: 2px solid #dee2e6;
            border-radius: var(--border-radius);
            font-size: var(--font-size);
            font-weight: bold;
            color: #333;
            cursor: pointer;
            transition: all 0.2s ease;
            position: relative;
        }}
        
        .cell:hover {{
            background: #e3f2fd;
            transform: scale(1.05);
            z-index: 10;
        }}
        
        .cell.selecting {{
            background: #bbdefb !important;
            border-color: #2196F3 !important;
            transform: scale(1.1);
            z-index: 100;
        }}
        
        .cell.found {{
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            border-color: #4CAF50;
        }}
        
        .words-section {{
            flex: 0 0 var(--words-section-width);
            min-width: 250px;
            max-height: 80vh;
            overflow-y: auto;
            overflow-x: hidden;
        }}

        .words-section::-webkit-scrollbar {{
            width: 8px;
        }}

        .words-section::-webkit-scrollbar-track {{
            background: #f1f1f1;
            border-radius: 10px;
        }}

        .words-section::-webkit-scrollbar-thumb {{
            background: #888;
            border-radius: 10px;
        }}

        .words-section::-webkit-scrollbar-thumb:hover {{
            background: #555;
        }}

        .words-title {{
            font-size: clamp(1.3em, 2vw, 1.8em);
            color: #333;
            margin-bottom: 20px;
            font-weight: bold;
            text-align: center;
            sticky: top 0;
            background: white;
            padding: 10px 0;
            z-index: 10;
        }}

        .words-list {{
            display: grid;
            grid-template-columns: repeat(var(--words-list-columns), 1fr);
            gap: var(--word-gap);
            padding-right: 5px;
        }}

        .word-item {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: var(--word-item-padding);
            border-radius: 10px;
            font-weight: bold;
            font-size: var(--word-item-font-size);
            box-shadow: 0 3px 8px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            cursor: default;
            text-align: center;
            word-break: break-word;
        }}
        
        .word-item:hover {{
            transform: translateX(5px);
        }}
        
        .word-item.found {{
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            text-decoration: line-through;
            opacity: 0.7;
        }}
        
        .stats {{
            margin-top: 30px;
            padding: 20px;
            background: #e3f2fd;
            border-radius: 12px;
            text-align: center;
        }}
        
        .stats h3 {{
            color: #333;
            margin-bottom: 10px;
        }}
        
        .progress {{
            font-size: 1.5em;
            color: #2196F3;
            font-weight: bold;
        }}
        
        .controls {{
            margin-top: 20px;
            text-align: center;
        }}
        
        button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }}
        
        button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.3);
        }}
        
        button:disabled {{
            opacity: 0.6;
            cursor: not-allowed;
        }}
        
        .victory {{
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.4);
            text-align: center;
            z-index: 1000;
            animation: popIn 0.5s ease;
        }}
        
        .victory.show {{
            display: block;
        }}
        
        .victory h2 {{
            color: #4CAF50;
            font-size: 2.5em;
            margin-bottom: 20px;
        }}
        
        .victory p {{
            font-size: 1.2em;
            color: #666;
        }}
        
        @keyframes popIn {{
            from {{
                transform: translate(-50%, -50%) scale(0.5);
                opacity: 0;
            }}
            to {{
                transform: translate(-50%, -50%) scale(1);
                opacity: 1;
            }}
        }}
        
        .overlay {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 999;
        }}

        .overlay.show {{
            display: block;
        }}

        /* Responsive adjustments for smaller screens */
        @media screen and (max-width: 768px) {{
            .container {{
                padding: 20px;
            }}

            .game-container {{
                gap: 20px;
            }}

            .grid-section {{
                min-width: 100%;
            }}

            .grid-container {{
                padding: 10px;
            }}

            h1 {{
                font-size: 1.8em;
            }}

            .words-section {{
                flex: 0 0 100%;
                width: 100%;
            }}

            .words-list {{
                grid-template-columns: 1fr !important;
            }}
        }}

        /* Extra scaling for very large grids */
        @media screen and (max-width: 1400px) {{
            :root {{
                --cell-size: {min(cell_size, 40)}px;
                --font-size: {min(font_size, 18)}px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 {title}</h1>
        <div class="subtitle">Click and drag to select words! Each game has a new puzzle.</div>
        
        <div class="game-container">
            <div class="grid-section">
                <div class="grid-container">
                    <div class="grid" id="grid">
"""
        
        # Add grid cells (will be populated by JavaScript)
        for row in range(self.size):
            for col in range(self.size):
                html_content += f'                        <div class="cell" data-row="{row}" data-col="{col}"></div>\n'
        
        html_content += """                    </div>
                </div>
                
                <div class="controls">
                    <button onclick="resetGame()">🎲 New Puzzle</button>
                </div>
            </div>
            
            <div class="words-section">
                <div class="words-title">Words to Find:</div>
                <div class="words-list" id="wordsList">
"""
        
        # Add words list
        for word in sorted(self.words):
            html_content += f'                    <div class="word-item" data-word="{word}">{word}</div>\n'
        
        html_content += f"""                </div>
                
                <div class="stats">
                    <h3>Progress</h3>
                    <div class="progress">
                        <span id="found">0</span> / <span id="total">{len(self.words)}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="overlay" id="overlay"></div>
    <div class="victory" id="victory">
        <h2>🎉 Congratulations! 🎉</h2>
        <p>You found all the words!</p>
        <br>
        <button onclick="resetGame()">🎲 New Puzzle</button>
    </div>
    
    <script>
        // All available puzzles
        const allPuzzles = {json.dumps(puzzles)};
        let currentPuzzleIndex = 0;
        
        // Current game state
        let wordData = {{}};
        let gridData = [];
        
        let isSelecting = false;
        let selectedCells = [];
        let foundWords = new Set();
        let selectionDirection = null;
        let startCell = null;
        
        const grid = document.getElementById('grid');
        let cells = grid.querySelectorAll('.cell');
        let wordItems = document.querySelectorAll('.word-item');
        let cellsArray = Array.from(cells);
        
        // Initialize with first puzzle
        loadPuzzle(0);
        
        // Add event listeners
        grid.addEventListener('mousedown', startSelection);
        grid.addEventListener('mouseover', continueSelection);
        document.addEventListener('mouseup', endSelection);
        
        // Touch support
        grid.addEventListener('touchstart', handleTouchStart, {{ passive: false }});
        grid.addEventListener('touchmove', handleTouchMove, {{ passive: false }});
        grid.addEventListener('touchend', endSelection);
        
        function loadPuzzle(index) {{
            const puzzle = allPuzzles[index % allPuzzles.length];
            gridData = puzzle.grid;
            wordData = puzzle.words;
            
            // Update grid display
            cellsArray.forEach((cell, i) => {{
                const row = Math.floor(i / {self.size});
                const col = i % {self.size};
                cell.textContent = gridData[row][col];
                cell.className = 'cell';
            }});
            
            // Reset game state
            foundWords.clear();
            selectedCells = [];
            
            // Reset word items
            wordItems.forEach(item => {{
                item.classList.remove('found');
            }});
            
            // Update progress
            updateProgress();
        }}
        
        function startSelection(e) {{
            if (e.target.classList.contains('cell')) {{
                isSelecting = true;
                selectedCells = [];
                selectionDirection = null;
                startCell = e.target;
                clearSelection();
                selectCell(e.target);
            }}
        }}
        
        function continueSelection(e) {{
            if (isSelecting && e.target.classList.contains('cell')) {{
                selectCell(e.target);
            }}
        }}
        
        function getDirection(fromCell, toCell) {{
            const fromRow = parseInt(fromCell.dataset.row);
            const fromCol = parseInt(fromCell.dataset.col);
            const toRow = parseInt(toCell.dataset.row);
            const toCol = parseInt(toCell.dataset.col);
            
            const rowDiff = toRow - fromRow;
            const colDiff = toCol - fromCol;
            
            const rowDir = rowDiff === 0 ? 0 : (rowDiff > 0 ? 1 : -1);
            const colDir = colDiff === 0 ? 0 : (colDiff > 0 ? 1 : -1);
            
            return {{ rowDir, colDir }};
        }}
        
        function isInLine(fromCell, toCell, direction) {{
            const fromRow = parseInt(fromCell.dataset.row);
            const fromCol = parseInt(fromCell.dataset.col);
            const toRow = parseInt(toCell.dataset.row);
            const toCol = parseInt(toCell.dataset.col);
            
            const rowDiff = toRow - fromRow;
            const colDiff = toCol - fromCol;
            
            if (direction.rowDir === 0 && direction.colDir === 0) return true;
            
            if (direction.rowDir === 0) {{
                return rowDiff === 0 && Math.sign(colDiff) === direction.colDir;
            }} else if (direction.colDir === 0) {{
                return colDiff === 0 && Math.sign(rowDiff) === direction.rowDir;
            }} else {{
                return Math.abs(rowDiff) === Math.abs(colDiff) && 
                       Math.sign(rowDiff) === direction.rowDir && 
                       Math.sign(colDiff) === direction.colDir;
            }}
        }}
        
        function selectCell(cell) {{
            if (selectedCells.includes(cell)) return;
            
            if (selectedCells.length === 0) {{
                selectedCells.push(cell);
                cell.classList.add('selecting');
                return;
            }}
            
            if (selectedCells.length === 1) {{
                const dir = getDirection(selectedCells[0], cell);
                if (Math.abs(dir.rowDir) <= 1 && Math.abs(dir.colDir) <= 1 && 
                    (dir.rowDir !== 0 || dir.colDir !== 0)) {{
                    selectionDirection = dir;
                    selectedCells.push(cell);
                    cell.classList.add('selecting');
                }}
                return;
            }}
            
            if (selectionDirection && isInLine(startCell, cell, selectionDirection)) {{
                const lastCell = selectedCells[selectedCells.length - 1];
                const cellsBetween = getCellsBetween(lastCell, cell, selectionDirection);
                
                cellsBetween.forEach(c => {{
                    if (!selectedCells.includes(c)) {{
                        selectedCells.push(c);
                        c.classList.add('selecting');
                    }}
                }});
                
                if (!selectedCells.includes(cell)) {{
                    selectedCells.push(cell);
                    cell.classList.add('selecting');
                }}
            }}
        }}
        
        function getCellsBetween(fromCell, toCell, direction) {{
            const cells = [];
            const fromRow = parseInt(fromCell.dataset.row);
            const fromCol = parseInt(fromCell.dataset.col);
            const toRow = parseInt(toCell.dataset.row);
            const toCol = parseInt(toCell.dataset.col);
            
            let currentRow = fromRow + direction.rowDir;
            let currentCol = fromCol + direction.colDir;
            
            while (currentRow !== toRow || currentCol !== toCol) {{
                const cell = cellsArray.find(c => 
                    parseInt(c.dataset.row) === currentRow && 
                    parseInt(c.dataset.col) === currentCol
                );
                if (cell) cells.push(cell);
                
                currentRow += direction.rowDir;
                currentCol += direction.colDir;
                
                if (Math.abs(currentRow - fromRow) > 20 || Math.abs(currentCol - fromCol) > 20) break;
            }}
            
            return cells;
        }}
        
        function endSelection() {{
            if (isSelecting) {{
                isSelecting = false;
                checkWord();
                clearSelection();
            }}
        }}
        
        function clearSelection() {{
            cellsArray.forEach(cell => cell.classList.remove('selecting'));
        }}
        
        function checkWord() {{
            if (selectedCells.length === 0) return;
            
            const selectedWord = selectedCells.map(cell => cell.textContent).join('');
            
            for (const [word, positions] of Object.entries(wordData)) {{
                if (foundWords.has(word)) continue;
                
                if (selectedWord === word && matchesPositions(selectedCells, positions)) {{
                    markWordFound(word, selectedCells);
                    return;
                }}
                
                const reversedWord = selectedWord.split('').reverse().join('');
                if (reversedWord === word && matchesPositions(selectedCells.slice().reverse(), positions)) {{
                    markWordFound(word, selectedCells);
                    return;
                }}
            }}
        }}
        
        function matchesPositions(cells, positions) {{
            if (cells.length !== positions.length) return false;
            
            return cells.every((cell, i) => {{
                const row = parseInt(cell.dataset.row);
                const col = parseInt(cell.dataset.col);
                return row === positions[i][0] && col === positions[i][1];
            }});
        }}
        
        function markWordFound(word, cells) {{
            foundWords.add(word);
            
            cells.forEach(cell => {{
                cell.classList.remove('selecting');
                cell.classList.add('found');
            }});
            
            const wordItem = document.querySelector(`.word-item[data-word="${{word}}"]`);
            if (wordItem) {{
                wordItem.classList.add('found');
            }}
            
            updateProgress();
            
            if (foundWords.size === Object.keys(wordData).length) {{
                setTimeout(showVictory, 500);
            }}
        }}
        
        function updateProgress() {{
            document.getElementById('found').textContent = foundWords.size;
        }}
        
        function showVictory() {{
            document.getElementById('overlay').classList.add('show');
            document.getElementById('victory').classList.add('show');
        }}
        
        function resetGame() {{
            // Load next puzzle
            currentPuzzleIndex++;
            loadPuzzle(currentPuzzleIndex);
            
            // Hide victory message
            document.getElementById('overlay').classList.remove('show');
            document.getElementById('victory').classList.remove('show');
        }}
        
        // Touch support functions
        function handleTouchStart(e) {{
            e.preventDefault();
            const touch = e.touches[0];
            const element = document.elementFromPoint(touch.clientX, touch.clientY);
            if (element && element.classList.contains('cell')) {{
                isSelecting = true;
                selectedCells = [];
                selectionDirection = null;
                startCell = element;
                clearSelection();
                selectCell(element);
            }}
        }}
        
        function handleTouchMove(e) {{
            e.preventDefault();
            if (isSelecting) {{
                const touch = e.touches[0];
                const element = document.elementFromPoint(touch.clientX, touch.clientY);
                if (element && element.classList.contains('cell')) {{
                    selectCell(element);
                }}
            }}
        }}
        
        // Initialize progress display
        document.getElementById('total').textContent = Object.keys(wordData).length;
    </script>
</body>
</html>"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n✓ Interactive HTML file exported: {filename}")
        print(f"✓ Generated {len(puzzles)} unique puzzles!")


def main():
    """
    Main function to demonstrate the multi-puzzle word search generator.
    """
    # Default words
    default_words = [
        "addobbo",    # decoration
        "angelo",     # angel
        "giuseppe",   # Joseph
        "cometa",     # comet
        "stella",     # star
        "maria",      # Mary
        "magi",       # wise men
        "betlemme",   # Bethlehem
        "bue",        # ox
        "natale",     # Christmas
        "asinello",   # little donkey
        "stalla"      # stable
    ]

    # Set up argument parser
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
        '--size',
        type=int,
        default=9,
        help='Grid size (default: 9)'
    )

    parser.add_argument(
        '--words',
        nargs='+',
        help='List of words to include in the puzzle (space-separated)'
    )

    parser.add_argument(
        '--wordfile',
        type=str,
        help='Path to a text file containing words (one per line)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='interactive_word_search.html',
        help='Output HTML filename (default: interactive_word_search.html)'
    )

    parser.add_argument(
        '--title',
        type=str,
        default='Word Search Puzzle',
        help='Puzzle title (default: Word Search Puzzle)'
    )

    parser.add_argument(
        '--count',
        type=int,
        default=10,
        help='Number of puzzles to generate (default: 10)'
    )

    args = parser.parse_args()

    # Determine which words to use
    words = default_words

    if args.wordfile:
        try:
            with open(args.wordfile, 'r', encoding='utf-8') as f:
                words = [line.strip() for line in f if line.strip()]
            print(f"✓ Loaded {len(words)} words from {args.wordfile}")
        except FileNotFoundError:
            print(f"✗ Error: File '{args.wordfile}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"✗ Error reading file: {e}")
            sys.exit(1)
    elif args.words:
        words = args.words
        print(f"✓ Using {len(words)} custom words")
    else:
        print(f"✓ Using default Christmas-themed words")

    # Validate inputs
    if len(words) == 0:
        print("✗ Error: No words provided.")
        sys.exit(1)

    if args.size < 5:
        print("✗ Error: Grid size must be at least 5.")
        sys.exit(1)

    if args.size > 30:
        print("✗ Error: Grid size must be at most 30 (for practical HTML rendering).")
        sys.exit(1)

    # Check if words fit in grid
    max_word_length = max(len(word) for word in words)
    if max_word_length > args.size:
        print(f"✗ Error: Longest word '{max(words, key=len)}' ({max_word_length} letters) won't fit in {args.size}x{args.size} grid.")
        print(f"   Increase grid size to at least {max_word_length} or use shorter words.")
        sys.exit(1)

    grid_size = args.size

    print(f"\nGenerating multiple {grid_size}x{grid_size} interactive word search puzzles...")
    print(f"Words to place: {len(words)}")
    print(f"Output file: {args.output}")
    print(f"Puzzle title: {args.title}")
    print(f"Number of puzzles: {args.count}")

    generator = MultiPuzzleWordSearchGenerator(grid_size, words)
    generator.export_multi_puzzle_html(args.output, args.title, puzzle_count=args.count)

    print("\n✓ Interactive puzzle generated successfully!")
    print("\n📝 Features:")
    print(f"   • {args.count} different unique puzzles pre-generated")
    print("   • Click 'New Puzzle' button to get a fresh puzzle")
    print("   • Smart directional locking for easy diagonal selection")
    print("   • Found words automatically highlight in green")
    print("   • Words are crossed off the list when found")
    print("   • Progress tracker shows how many words found")
    print("   • Victory celebration when all words are found")


if __name__ == "__main__":
    main()
