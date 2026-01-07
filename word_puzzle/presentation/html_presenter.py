"""
Presentation Layer - HTML Presenter
Transforms domain models into HTML format
"""
from typing import List, Dict, Any
from dataclasses import dataclass
import json
from ..domain import Puzzle, Position
from ..application.interfaces import IPuzzlePresenter


@dataclass
class GridStyling:
    """Styling configuration for puzzle grid."""
    cell_size: int
    font_size: int
    gap: int
    border_radius: int


@dataclass
class WordListStyling:
    """Styling configuration for word list."""
    item_padding: str
    item_font_size: str
    gap: str
    section_width: str
    columns: str


class StylingCalculator:
    """Calculates responsive styling based on grid and word list parameters."""

    @staticmethod
    def calculate_grid_styling(grid_size: int) -> GridStyling:
        """Calculate grid styling based on grid size."""
        if grid_size <= 10:
            return GridStyling(50, 22, 3, 8)
        elif grid_size <= 15:
            return GridStyling(45, 20, 3, 6)
        elif grid_size <= 20:
            return GridStyling(35, 16, 2, 5)
        else:
            return GridStyling(28, 14, 2, 4)

    @staticmethod
    def calculate_word_list_styling(word_count: int) -> WordListStyling:
        """Calculate word list styling based on word count."""
        if word_count <= 10:
            return WordListStyling("15px 20px", "1.2em", "12px", "300px", "1")
        elif word_count <= 20:
            return WordListStyling("12px 16px", "1.1em", "10px", "320px", "1")
        elif word_count <= 30:
            return WordListStyling("10px 14px", "1em", "8px", "380px", "2")
        else:
            return WordListStyling("8px 12px", "0.95em", "6px", "450px", "2")

    @staticmethod
    def calculate_container_max_width(
        grid_size: int,
        grid_styling: GridStyling,
        word_styling: WordListStyling
    ) -> int:
        """Calculate maximum container width."""
        grid_width = (grid_size * grid_styling.cell_size +
                     (grid_size - 1) * grid_styling.gap + 40)
        words_width = int(word_styling.section_width.replace('px', ''))
        return max(1200, grid_width + words_width + 100)


class HTMLTemplateBuilder:
    """Builds HTML template components."""

    @staticmethod
    def build_css_styles(grid_size: int, word_count: int) -> str:
        """Build CSS styles for the puzzle."""
        grid_styling = StylingCalculator.calculate_grid_styling(grid_size)
        word_styling = StylingCalculator.calculate_word_list_styling(word_count)
        container_width = StylingCalculator.calculate_container_max_width(
            grid_size, grid_styling, word_styling
        )

        return f"""        :root {{
            --cell-size: {grid_styling.cell_size}px;
            --font-size: {grid_styling.font_size}px;
            --grid-gap: {grid_styling.gap}px;
            --border-radius: {grid_styling.border_radius}px;
            --word-item-padding: {word_styling.item_padding};
            --word-item-font-size: {word_styling.item_font_size};
            --word-gap: {word_styling.gap};
            --words-section-width: {word_styling.section_width};
            --words-list-columns: {word_styling.columns};
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

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
            max-width: {container_width}px;
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
            grid-template-columns: repeat({grid_size}, var(--cell-size));
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

        .cell:hover {{ background: #e3f2fd; transform: scale(1.05); z-index: 10; }}
        .cell.selecting {{ background: #bbdefb !important; border-color: #2196F3 !important; transform: scale(1.1); z-index: 100; }}
        .cell.found {{ background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); color: white; border-color: #4CAF50; }}

        .words-section {{
            flex: 0 0 var(--words-section-width);
            min-width: 250px;
            max-height: 80vh;
            overflow-y: auto;
            overflow-x: hidden;
        }}

        .words-section::-webkit-scrollbar {{ width: 8px; }}
        .words-section::-webkit-scrollbar-track {{ background: #f1f1f1; border-radius: 10px; }}
        .words-section::-webkit-scrollbar-thumb {{ background: #888; border-radius: 10px; }}
        .words-section::-webkit-scrollbar-thumb:hover {{ background: #555; }}

        .words-title {{
            font-size: clamp(1.3em, 2vw, 1.8em);
            color: #333;
            margin-bottom: 20px;
            font-weight: bold;
            text-align: center;
            position: sticky;
            top: 0;
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

        .word-item:hover {{ transform: translateX(5px); }}
        .word-item.found {{ background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); text-decoration: line-through; opacity: 0.7; }}

        .stats {{
            margin-top: 30px;
            padding: 20px;
            background: #e3f2fd;
            border-radius: 12px;
            text-align: center;
        }}

        .stats h3 {{ color: #333; margin-bottom: 10px; }}
        .progress {{ font-size: 1.5em; color: #2196F3; font-weight: bold; }}

        .controls {{ margin-top: 20px; text-align: center; }}

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

        button:hover {{ transform: translateY(-2px); box-shadow: 0 6px 12px rgba(0,0,0,0.3); }}
        button:disabled {{ opacity: 0.6; cursor: not-allowed; }}

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

        .victory.show {{ display: block; }}
        .victory h2 {{ color: #4CAF50; font-size: 2.5em; margin-bottom: 20px; }}
        .victory p {{ font-size: 1.2em; color: #666; }}

        @keyframes popIn {{
            from {{ transform: translate(-50%, -50%) scale(0.5); opacity: 0; }}
            to {{ transform: translate(-50%, -50%) scale(1); opacity: 1; }}
        }}

        .overlay {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 999; }}
        .overlay.show {{ display: block; }}

        @media screen and (max-width: 768px) {{
            .container {{ padding: 20px; }}
            .game-container {{ gap: 20px; }}
            .grid-section {{ min-width: 100%; }}
            .grid-container {{ padding: 10px; }}
            h1 {{ font-size: 1.8em; }}
            .words-section {{ flex: 0 0 100%; width: 100%; }}
            .words-list {{ grid-template-columns: 1fr !important; }}
        }}

        @media screen and (max-width: 1400px) {{
            :root {{
                --cell-size: {min(grid_styling.cell_size, 40)}px;
                --font-size: {min(grid_styling.font_size, 18)}px;
            }}
        }}"""

    @staticmethod
    def build_grid_cells(grid_size: int) -> str:
        """Build HTML for grid cells."""
        cells = ""
        for row in range(grid_size):
            for col in range(grid_size):
                cells += f'                        <div class="cell" data-row="{row}" data-col="{col}"></div>\n'
        return cells

    @staticmethod
    def build_word_list(words: List[str]) -> str:
        """Build HTML for word list."""
        words_html = ""
        for word in sorted(words):
            words_html += f'                    <div class="word-item" data-word="{word}">{word}</div>\n'
        return words_html

    @staticmethod
    def build_javascript(puzzles_data: List[Dict], grid_size: int) -> str:
        """Build JavaScript code for puzzle interactivity."""
        # JavaScript code from original implementation (kept as is for brevity)
        return f"""        const allPuzzles = {json.dumps(puzzles_data)};
        let currentPuzzleIndex = 0;
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

        loadPuzzle(0);

        grid.addEventListener('mousedown', startSelection);
        grid.addEventListener('mouseover', continueSelection);
        document.addEventListener('mouseup', endSelection);
        grid.addEventListener('touchstart', handleTouchStart, {{ passive: false }});
        grid.addEventListener('touchmove', handleTouchMove, {{ passive: false }});
        grid.addEventListener('touchend', endSelection);

        function loadPuzzle(index) {{
            const puzzle = allPuzzles[index % allPuzzles.length];
            gridData = puzzle.grid;
            wordData = puzzle.words;
            cellsArray.forEach((cell, i) => {{
                const row = Math.floor(i / {grid_size});
                const col = i % {grid_size};
                cell.textContent = gridData[row][col];
                cell.className = 'cell';
            }});
            foundWords.clear();
            selectedCells = [];
            wordItems.forEach(item => item.classList.remove('found'));
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
            if (isSelecting && e.target.classList.contains('cell')) selectCell(e.target);
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
            if (direction.rowDir === 0) return rowDiff === 0 && Math.sign(colDiff) === direction.colDir;
            else if (direction.colDir === 0) return colDiff === 0 && Math.sign(rowDiff) === direction.rowDir;
            else return Math.abs(rowDiff) === Math.abs(colDiff) && Math.sign(rowDiff) === direction.rowDir && Math.sign(colDiff) === direction.colDir;
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
                if (Math.abs(dir.rowDir) <= 1 && Math.abs(dir.colDir) <= 1 && (dir.rowDir !== 0 || dir.colDir !== 0)) {{
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
                const cell = cellsArray.find(c => parseInt(c.dataset.row) === currentRow && parseInt(c.dataset.col) === currentCol);
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

        function clearSelection() {{ cellsArray.forEach(cell => cell.classList.remove('selecting')); }}

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
            if (wordItem) wordItem.classList.add('found');
            updateProgress();
            if (foundWords.size === Object.keys(wordData).length) setTimeout(showVictory, 500);
        }}

        function updateProgress() {{ document.getElementById('found').textContent = foundWords.size; }}

        function showVictory() {{
            document.getElementById('overlay').classList.add('show');
            document.getElementById('victory').classList.add('show');
        }}

        function resetGame() {{
            currentPuzzleIndex++;
            loadPuzzle(currentPuzzleIndex);
            document.getElementById('overlay').classList.remove('show');
            document.getElementById('victory').classList.remove('show');
        }}

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
                if (element && element.classList.contains('cell')) selectCell(element);
            }}
        }}

        document.getElementById('total').textContent = Object.keys(wordData).length;"""


class HTMLPuzzlePresenter(IPuzzlePresenter):
    """Presenter for transforming puzzles into HTML format."""

    def present(self, puzzles: List[Puzzle], metadata: Dict[str, Any]) -> str:
        """Present puzzles as an HTML document."""
        if not puzzles:
            raise ValueError("No puzzles to present")

        first_puzzle = puzzles[0]
        title = metadata.get('title', 'Word Search Puzzle')

        # Convert puzzles to JSON-serializable format
        puzzles_data = self._convert_puzzles_to_data(puzzles)

        # Build HTML components
        css = HTMLTemplateBuilder.build_css_styles(
            first_puzzle.grid_size,
            len(first_puzzle.words)
        )
        grid_cells = HTMLTemplateBuilder.build_grid_cells(first_puzzle.grid_size)
        word_list = HTMLTemplateBuilder.build_word_list(
            [str(w) for w in first_puzzle.words]
        )
        javascript = HTMLTemplateBuilder.build_javascript(
            puzzles_data,
            first_puzzle.grid_size
        )

        # Assemble complete HTML document
        return self._build_html_document(
            title, css, grid_cells, word_list, javascript, len(first_puzzle.words)
        )

    def _convert_puzzles_to_data(self, puzzles: List[Puzzle]) -> List[Dict]:
        """Convert puzzle entities to JSON-serializable data."""
        puzzles_data = []
        for puzzle in puzzles:
            word_data = {}
            for placement in puzzle.placements:
                positions = [[pos.row, pos.col] for pos in placement.positions]
                word_data[str(placement.word)] = positions

            puzzles_data.append({
                'grid': puzzle.grid,
                'words': word_data
            })
        return puzzles_data

    def _build_html_document(
        self, title: str, css: str, grid_cells: str,
        word_list: str, javascript: str, word_count: int
    ) -> str:
        """Build complete HTML document."""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
{css}
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
{grid_cells}                    </div>
                </div>
                <div class="controls">
                    <button onclick="resetGame()">🎲 New Puzzle</button>
                </div>
            </div>
            <div class="words-section">
                <div class="words-title">Words to Find:</div>
                <div class="words-list" id="wordsList">
{word_list}                </div>
                <div class="stats">
                    <h3>Progress</h3>
                    <div class="progress">
                        <span id="found">0</span> / <span id="total">{word_count}</span>
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
{javascript}
    </script>
</body>
</html>"""
