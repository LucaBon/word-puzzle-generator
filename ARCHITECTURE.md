# Clean Architecture Documentation

## Overview

This project follows Clean Architecture principles, ensuring a clear separation of concerns and proper dependency management.

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│  (CLI Controller, HTML Presenter)                           │
│  - User Interface                                           │
│  - Output Formatting                                        │
└──────────────────────┬──────────────────────────────────────┘
                       │ depends on ↓
┌─────────────────────────────────────────────────────────────┐
│                   Infrastructure Layer                       │
│  (Repositories, Validators)                                 │
│  - External Interfaces                                      │
│  - Framework/Library Specific Code                          │
└──────────────────────┬──────────────────────────────────────┘
                       │ depends on ↓
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
│  (Use Cases, Services, Interfaces)                          │
│  - Application Business Rules                               │
│  - Use Case Orchestration                                   │
└──────────────────────┬──────────────────────────────────────┘
                       │ depends on ↓
┌─────────────────────────────────────────────────────────────┐
│                      Domain Layer                            │
│  (Entities, Value Objects)                                  │
│  - Enterprise Business Rules                                │
│  - Core Business Logic                                      │
│  - NO external dependencies                                 │
└─────────────────────────────────────────────────────────────┘
```

## Layer Descriptions

### 1. Domain Layer (Innermost)
**Location**: `word_puzzle/domain/`

**Purpose**: Contains the core business logic and rules

**Components**:
- **Entities** (`entities.py`):
  - `Puzzle`: Represents a complete word search puzzle
  - `WordPlacement`: Represents a word placed in the grid

- **Value Objects** (`value_objects.py`):
  - `Word`: Immutable word representation
  - `Position`: Immutable grid position
  - `Direction`: Immutable direction vector
  - `GridSize`: Validated grid size
  - `Directions`: Factory for standard directions

**Key Principles**:
- No dependencies on outer layers
- Pure business logic
- Immutable where appropriate
- Self-validating

### 2. Application Layer
**Location**: `word_puzzle/application/`

**Purpose**: Orchestrates business logic and defines interfaces

**Components**:
- **Use Cases** (`use_cases.py`):
  - `GeneratePuzzleUseCase`: Orchestrates puzzle generation
  - `ValidateConfigUseCase`: Validates puzzle configuration

- **Services** (`services.py`):
  - `DirectionBalancer`: Balances word placement directions
  - `WordPlacementService`: Handles word placement logic
  - `PuzzleGenerationStrategy`: Strategy for generating puzzles

- **Interfaces** (`interfaces.py`):
  - `IPuzzleRepository`: Interface for puzzle persistence
  - `IWordRepository`: Interface for word data access
  - `IPuzzlePresenter`: Interface for puzzle presentation
  - `IConfigValidator`: Interface for validation

**Key Principles**:
- Depends only on domain layer
- Defines abstract interfaces (ports)
- Contains application-specific business rules
- Framework-independent

### 3. Infrastructure Layer
**Location**: `word_puzzle/infrastructure/`

**Purpose**: Implements interfaces with external dependencies

**Components**:
- **Repositories** (`repositories.py`):
  - `FileWordRepository`: Loads words from files
  - `HTMLFileRepository`: Saves puzzles as HTML files

- **Validators** (`validators.py`):
  - `PuzzleConfigValidator`: Validates puzzle configuration

**Key Principles**:
- Implements application layer interfaces
- Contains framework-specific code
- Handles external dependencies (file system, etc.)
- Easily replaceable

### 4. Presentation Layer (Outermost)
**Location**: `word_puzzle/presentation/`

**Purpose**: Handles user interaction and output formatting

**Components**:
- **Controllers** (`cli_controller.py`):
  - `CLIController`: Command-line interface controller

- **Presenters** (`html_presenter.py`):
  - `HTMLPuzzlePresenter`: Transforms puzzles to HTML
  - `HTMLTemplateBuilder`: Builds HTML components
  - `StylingCalculator`: Calculates responsive styles

**Key Principles**:
- Depends on application layer
- Handles user input/output
- Framework-specific UI code
- Easily replaceable with other UIs (web, GUI, etc.)

## Dependency Flow

```
main.py (Composition Root)
   ↓
   Creates all dependencies
   ↓
   ┌─────────────────────────────────────────┐
   │  Dependency Injection Container         │
   ├─────────────────────────────────────────┤
   │  1. Infrastructure (Repositories, etc.) │
   │  2. Presentation (Presenters)           │
   │  3. Application (Use Cases)             │
   │  4. Presentation (Controllers)          │
   └─────────────────────────────────────────┘
```

## Key Design Patterns

### 1. Dependency Inversion Principle (DIP)
- Application layer defines interfaces
- Infrastructure implements these interfaces
- Dependencies point inward (toward domain)

### 2. Dependency Injection (DI)
- `main.py` acts as the composition root
- All dependencies are injected through constructors
- No hard-coded dependencies

### 3. Use Case Pattern
- Each user action is a separate use case
- Use cases orchestrate business logic
- Clear input/output boundaries

### 4. Repository Pattern
- Abstract data access behind interfaces
- Domain layer unaware of data source
- Easy to swap implementations

### 5. Strategy Pattern
- `PuzzleGenerationStrategy`: Different generation algorithms
- Easily extendable with new strategies

### 6. Presenter Pattern
- Transforms domain models to presentation format
- Separates business logic from presentation

## Benefits of This Architecture

### 1. **Testability**
- Easy to unit test each layer independently
- Mock/stub external dependencies
- Domain logic testable without UI or database

### 2. **Maintainability**
- Clear separation of concerns
- Easy to locate and modify code
- Changes in one layer don't affect others

### 3. **Flexibility**
- Easy to add new UI (web, desktop, mobile)
- Easy to change persistence (database, cloud)
- Easy to add new use cases

### 4. **Independence**
- **Framework Independent**: Domain doesn't depend on frameworks
- **Database Independent**: Can swap file storage for database
- **UI Independent**: Can replace CLI with web UI

### 5. **Business Logic Protection**
- Core business rules isolated in domain
- Protected from external changes
- Reusable across applications

## Testing Strategy

### Domain Layer
```python
# Test entities and value objects in isolation
def test_puzzle_can_place_word():
    puzzle = Puzzle(grid_size=5, words=[Word("HELLO")])
    position = Position(0, 0)
    direction = Directions.HORIZONTAL_RIGHT
    assert puzzle.can_place_word(Word("HELLO"), position, direction)
```

### Application Layer
```python
# Test use cases with mocked dependencies
def test_generate_puzzle_use_case():
    mock_repo = MockWordRepository()
    use_case = GeneratePuzzleUseCase(mock_repo, ...)
    response = use_case.execute(request)
    assert response.success
```

### Infrastructure Layer
```python
# Test concrete implementations
def test_file_word_repository():
    repo = FileWordRepository()
    words = repo.load_from_file("test.txt")
    assert len(words) > 0
```

### Integration Tests
```python
# Test the complete flow
def test_end_to_end_puzzle_generation():
    app = create_app()
    exit_code = app.run(["--size", "10", "--count", "1"])
    assert exit_code == 0
```

## How to Extend

### Adding a New Output Format (e.g., PDF)

1. **Create PDF Presenter** (Presentation Layer):
```python
class PDFPuzzlePresenter(IPuzzlePresenter):
    def present(self, puzzles, metadata):
        # Generate PDF
        pass
```

2. **Wire it up in main.py**:
```python
pdf_presenter = PDFPuzzlePresenter()
use_case = GeneratePuzzleUseCase(
    presenter=pdf_presenter,
    # ... other dependencies
)
```

### Adding a Web UI

1. **Create Web Controller** (Presentation Layer):
```python
class WebController:
    def __init__(self, use_case):
        self.use_case = use_case

    def generate_puzzle_endpoint(self, request):
        # Handle web request
        pass
```

2. **No changes needed** in domain or application layers!

### Adding Database Storage

1. **Create Database Repository** (Infrastructure Layer):
```python
class DatabasePuzzleRepository(IPuzzleRepository):
    def save(self, puzzle, identifier):
        # Save to database
        pass
```

2. **Wire it up in main.py**:
```python
puzzle_repo = DatabasePuzzleRepository()
```

## File Structure

```
word_puzzle/
├── __init__.py
├── domain/
│   ├── __init__.py
│   ├── entities.py          # Puzzle, WordPlacement
│   └── value_objects.py     # Word, Position, Direction, etc.
├── application/
│   ├── __init__.py
│   ├── interfaces.py        # Abstract interfaces (ports)
│   ├── services.py          # Domain services
│   └── use_cases.py         # Use case implementations
├── infrastructure/
│   ├── __init__.py
│   ├── repositories.py      # Concrete repository implementations
│   └── validators.py        # Validation implementations
└── presentation/
    ├── __init__.py
    ├── cli_controller.py    # CLI interface
    └── html_presenter.py    # HTML presentation logic

main.py                      # Composition root (DI container)
```

## Clean Architecture Principles Applied

1. **Independence of Frameworks**: The core business logic doesn't depend on any framework
2. **Testability**: Business rules can be tested without UI, database, or external elements
3. **Independence of UI**: The UI can change without changing the rest of the system
4. **Independence of Database**: Business rules are not bound to a specific database
5. **Independence of External Agencies**: Business rules don't know about external interfaces

## Comparison with Previous Version

| Aspect | Before | After (Clean Architecture) |
|--------|--------|---------------------------|
| **Structure** | Single file, monolithic class | Layered architecture, multiple modules |
| **Dependencies** | Tightly coupled | Dependency inversion, loose coupling |
| **Testability** | Hard to test in isolation | Easy to mock and test each layer |
| **Extensibility** | Hard to add new features | Easy to extend with new use cases |
| **Business Logic** | Mixed with UI and persistence | Isolated in domain layer |
| **Reusability** | Low - tied to specific UI | High - core logic reusable |

## References

- [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) by Robert C. Martin
- [Domain-Driven Design](https://www.domainlanguage.com/ddd/) by Eric Evans
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) by Alistair Cockburn
