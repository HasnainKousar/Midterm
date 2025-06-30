# Midterm Project: Enhanced Calculator Command-Line Application

A command-line calculator application built with Python, featuring a Read-Eval-Print Loop (REPL) interface, comprehensive history management, undo/redo functionality, and colorized output.

## 📋 Table of Contents



## 🚀 Project Description
This enhanced calculator application provides a mathematical computation platform with an interactive command-line interface. Built using Python design patterns including the Factory Pattern, Observer Pattern, and Memento Pattern, it offers functionality for mathematical operations, history tracking, and session management with undo/redo capabilities.

### Key Architectural Features
- **REPL Interface**: Interactive command-line environment with colorized output
- **Design Patterns**: Implementation of Factory, Observer, and Memento patterns
- **History Management**: Persistent calculation history with CSV storage
- **Undo/Redo Functionality**: Complete operation state management
- **Configuration Management**: Environment-based configuration system
- **Comprehensive Testing**: 100% test coverage with pytest (90%+ required)
- **CI/CD Pipeline**: Automated testing with GitHub Actions


## ✨ Features

## Mathematical Operations
- **Basic Arithmetic**: Addition, Subtraction, Multiplication, Division
- **Advanced Operations**: Power, Root, Modulus, Integer Division, Percentage, Absolute Difference

### User Interface Features
- **Colorized Output**: Green for normal operations, red for errors
- **Interactive REPL**: Command-line interface with real-time feedback
- **Error Handling**: Comprehensive error messages and recovery

### Data Management
- **Persistent History**: CSV-based calculation storage
- **Session Management**: Load and save calculation 
- **Undo/Redo**: Operation state management
- **Auto-save**: Automatic history saving

### Development Features
- **Comprehensive Testing**: Unit tests with 100% coverage
- **Logging System**: Configurable logging 
- **Configuration Management**: Environment variable based setup
- **CI/CD Pipeline**: Automated testing and validation


## 🛠 Installation Instructions

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd midterm
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip if necessary
python -m pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
# Run tests to verify installation
pytest

# Start VSCode (optional)
code .

# Start the calculator
python main.py
```


## ⚙️ Configuration Setup

### Creating the .env File

The application uses environment variables for configuration.

```bash
# Create .env file in the project root
touch .env
```
**Note**: The `.env` file is optional. 

### Environment Variables

Add the following variables to your `.env` file:

```env
# Logging Configuration
CALCULATOR_LOG_LEVEL=INFO
CALCULATOR_LOG_FILE=./logs/calculator.log

# History Configuration
CALCULATOR_HISTORY_FILE=./history/calculator_history.csv
CALCULATOR_AUTO_SAVE=true

# Application Configuration
CALCULATOR_PRECISION=10
CALCULATOR_BASE_DIR=.
```


### How .env Configuration Works in This Project

The calculator application uses the **python-dotenv** library to load environment variables from a `.env` file. Here's how it works:

1. **Automatic Loading**: When the application starts, `load_dotenv()` in `app/calculator_config.py` automatically reads the `.env` file
2. **Fallback to Defaults**: If a variable isn't found in `.env`, the application uses sensible defaults


## 📖 Usage Guide

### Starting the Calculator

```bash
python main.py
```

### Basic Operations

The calculator supports the following mathematical operations:

#### Arithmetic Operations
```
Enter command: add
Enter number (or cancel to abort): 5
First number: Second number: 3
Result: 8

Enter command: subtract
Enter number (or cancel to abort): 10
First number: Second number: 4
Result: 6
```

#### Available Operation Commands

| Command | Description | Example |
|---------|-------------|---------|
| `add` | Addition | `5 + 3 = 8` |
| `subtract` | Subtraction | `10 - 4 = 6` |
| `multiply` | Multiplication | `6 * 7 = 42` |
| `divide` | Division | `15 / 3 = 5` |
| `power` | Exponentiation | `2 ^ 3 = 8` |
| `root` | Root calculation | `√16 = 4` |
| `modulus` | Remainder | `10 % 3 = 1` |
| `integerdivision` | Integer division | `10 // 3 = 3` |
| `percentage` | Percentage | `25% of 200 = 50` |
| `absolutedifference` | Absolute difference | `\|5 - 8\| = 3` |

#### View Calculation History
```
Enter command: history
Calculation History:
1. Addition(5, 3) = 8
2. Subtraction(10, 4) = 6
```

#### Clear History
```
Enter command: clear
History cleared.
```

#### Save History
```
Enter command: save
History saved successfully.
```

#### Load History
```
Enter command: load
History loaded successfully.
```

#### Undo Last Operation
```
Enter command: undo
Last operation undone.
```

#### Redo Last Operation
```
Enter command: redo
Last operation redone.
```

#### Get Help
```
Enter command: help
Available commands:
  add, subtract, multiply, divide, power, root, modulus, integerdivision, percentage, absolutedifference
  history - Show calculation history
  undo - Undo the last operation
  redo - Redo the last undone operation
  clear - Clear the history
  save - Save the current history to a file
  load - Load history from a file
  exit - Exit the calculator REPL
```

#### Exit Calculator
```
Enter command: exit
History saved successfully.
Exiting calculator REPL. Goodbye!
```

#### Cancel Operation
Cancel any operation during number input:
```
Enter command: add
Enter number (or cancel to abort): cancel
Operation cancelled.
```

#### Error Handling

The calculator provides clear error messages:
```
Enter command: divide
Enter number (or cancel to abort): 5
First number: Second number: 0
Error: Division by zero is not allowed.
```

## 🧪 Testing Instructions

### Running Basic Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_calculator.py
```

### Test Coverage

```bash
# Run tests with coverage report (automatically included)
pytest

# View detailed HTML coverage report in browser (need live server extension)
open htmlcov/index.html
```

**Note**: Coverage reporting is automatically enabled in this project through `pytest.ini` configuration. Every time you run `pytest`, you'll see:
- Test results
- Coverage percentage
- Missing lines report
- HTML report generated in `htmlcov/` directory

### Coverage Requirements

The project maintains a **90% minimum test coverage** requirement. The CI/CD pipeline will fail if coverage drops below this threshold.


#### Test Files
- **Calculator Core**: `tests/test_calculator.py`
- **Operations**: `tests/test_operations.py`
- **Configuration**: `tests/test_config.py`
- **History Management**: `tests/test_history.py`
- **REPL Interface**: `tests/test_calculator_repl.py`
- **Calculations**: `tests/test_calculation.py`

