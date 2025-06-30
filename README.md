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



### Directory Structure Setup

