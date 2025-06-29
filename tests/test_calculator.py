###########################
# tests/test_calculator.py
###########################

"""


"""

import datetime
import logging
from pathlib import Path
import pandas as pd
import pytest
from unittest.mock import Mock, patch, PropertyMock
from decimal import Decimal
from tempfile import TemporaryDirectory

from app.calculator import Calculator
from app.calculator_repl import start_calculator_repl
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError
from app.history import LoggingObserver, AutoSaverObserver
from app.operations import OperationFactory

# fixute to create a temporary directory for testing
@pytest.fixture
def calculator():
    """ """
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        config = CalculatorConfig(base_dir=temp_path)

        # patch properties to use the temporary directory
        with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
             patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file, \
             patch.object(CalculatorConfig, 'history_dir', new_callable=PropertyMock) as mock_history_dir, \
             patch.object(CalculatorConfig, 'history_file', new_callable=PropertyMock) as mock_history_file:
            
            # set the mock return values to the temporary directory
            mock_log_dir.return_value = temp_path / 'logs'
            mock_log_file.return_value = temp_path / 'logs' / 'calculator.log'
            mock_history_dir.return_value = temp_path / 'history'
            mock_history_file.return_value = temp_path / 'history' / 'calculator_history.csv'

            # return a Calculator instance with the mocked config
            yield Calculator(config=config)

#  Test for Calculator initialization
def test_calculator_initialization(calculator):
    """ """
    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []
    assert calculator.operation_strategy is None




# Test Logging Setup

@patch('app.calculator.logging.info')
def test_logging_setup(logging_info_mock):
    with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
         patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file:
        
        mock_log_dir.return_value = Path('/tmp/logs')
        mock_log_file.return_value = Path('/tmp/logs/calculator.log')

        # Instantiate the calculator to trigger logging setup
        calculator = Calculator(CalculatorConfig())
        logging_info_mock.assert_any_call("Calculator initialized with configuration")

# Test for logging setup failed
@patch('builtins.print')
def test_setup_logging_failed(mock_print):
    """Test that logging setup fails gracefully."""
    with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
         patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file:
        
        mock_log_dir.return_value = Path('./test_logs')
        mock_log_file.return_value = Path('./test_logs/calculator.log')

        # Mock the logging setup to raise an exception
        with patch('app.calculator.logging.basicConfig') as mock_logging_config:
            mock_logging_config.side_effect = Exception("Logging setup failed")
            
            # Attempt to initialize the calculator
            with pytest.raises(Exception, match="Logging setup failed"):
                Calculator(CalculatorConfig())
            
            # Verify that the error message was printed
            mock_print.assert_called_once_with("Error setting up logging: Logging setup failed")

    
# Test for logging history failed
@patch('app.calculator.logging.warning')
@patch('app.calculator.logging.info')
def test_calculator_init_logging_history_failed(logging_info_mock, logging_warning_mock):
    """Test that logging setup is called during calculator initialization."""
    with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
         patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file:
        
        mock_log_dir.return_value = Path('/tmp/logs')
        mock_log_file.return_value = Path('/tmp/logs/calculator.log')

        # Mock the load_history to raise an exception
        with patch.object(Calculator, 'load_history') as mock_load_history:
            mock_load_history.side_effect = Exception("Failed to load history")
            
            calculator = Calculator(CalculatorConfig())
            
            # Verify the warning was logged
            logging_warning_mock.assert_called_once_with("Failed to load existing history: Failed to load history")
            # Verify initialization still completed successfully
            logging_info_mock.assert_any_call("Calculator initialized with configuration")

        
# Test for adding, removing and notifying observers
def test_add_observer(calculator):
    """Test for adding an observer."""
    observer = LoggingObserver()
    calculator.add_observer(observer)
    assert observer in calculator.observers

def test_remove_observer(calculator):
    """Test for removing an observer."""
    observer = LoggingObserver()
    calculator.add_observer(observer)
    calculator.remove_observer(observer)
    assert observer not in calculator.observers

def test_notify_observers(calculator):
    """Test for notifying observers."""
    observer = LoggingObserver()
    calculator.add_observer(observer)
    # Mock a calculation to notify observers
    calculation = Mock()
    calculation.operation = 'Addition'
    calculation.operand1 = Decimal('3')
    calculation.operand2 = Decimal('4')
    calculation.result = Decimal('7')
    # Notify observers
    calculator.notify_observers(calculation)
    # Check that the observer's update method was called
    observer.update(calculation)  # This should not raise an error


# Test for performing operations
def test_perform_operation_addition(calculator):
    """Test for performing addition operation."""
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    result = calculator.perform_operation(5, 4)
    assert result == Decimal('9')

def test_perform_operation_validation_error(calculator):
    """Test for validation error when performing operation."""
    calculator.set_operation(OperationFactory.create_operation('add'))
    with pytest.raises(ValidationError):
        calculator.perform_operation("five", 4)


def test_perform_operation_operation_error(calculator):
    """Test for operation error when no operation is set."""
    with pytest.raises(OperationError, match="No operation set. Please set an operation before performing calculations."):
        calculator.perform_operation(5, 4)

def test_perform_operation_exception(calculator):
    """Test for exception when performing operation."""
    # Create a mock operation that raises an exception
    operation = Mock()
    operation.perform.side_effect = Exception("Operation failed")
    calculator.set_operation(operation)
    
    with pytest.raises(OperationError, match="Operation failed"):
        calculator.perform_operation(5, 4)



# Test for undo and redo operations
def test_undo_operation(calculator):
    """Test for undoing an operation."""
    # create an operation and perform it
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(5, 4)
    # undo the operation
    calculator.undo()
    # check that the history is empty after undo
    assert len(calculator.history) == 0


def test_redo_operation(calculator):
    """Test for redoing an operation."""
    # create an operation and perform it
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(5, 4)
    # undo the operation
    calculator.undo()
    # redo the operation
    calculator.redo()
    # check that the history has one entry after redo
    assert len(calculator.history) == 1
   

# Test for saving and loading history
@patch('app.calculator.pd.DataFrame.to_csv')
def test_save_history(mock_to_csv, calculator):
    """Test for saving history to CSV file."""
    # create an operation and perform it
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(5, 4)
    
    # save the history
    calculator.save_history()
    
    # check that to_csv was called
    mock_to_csv.assert_called_once()

@patch('app.calculator.pd.read_csv')
@patch('app.calculator.Path.exists', return_value=True)
def test_load_history(mock_exists, mock_read_csv, calculator):
    """Test for loading history from CSV file."""
    # mock CSV data to match expected format in from_dict
    mock_read_csv.return_value = pd.DataFrame({
        'operation': ['Addition'],
        'operand1': ['3'],
        'operand2': ['4'],
        'result': ['7'],
        'timestamp': [datetime.datetime.now().isoformat()]
    })

    # Test loading history functionality
    try:
        calculator.load_history()
        # Verify the loaded history
        assert calculator.history[0].operation == 'Addition'
        assert calculator.history[0].operand1 == Decimal('3')
        assert calculator.history[0].operand2 == Decimal('4')
        assert calculator.history[0].result == Decimal('7')
    except OperationError:
        pytest.fail("Loading history raised an OperationError unexpectedly")

def test_clear_history(calculator):
    """Test for clearing the history."""
    # create an operation and perform it
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(5, 4)
    
    # clear the history
    calculator.clear_history()
    
    # check that the history is empty
    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []

def test_save_history_with_empty_history(calculator):
    """Test saving history when history is empty."""
    # Clear the history
    calculator.clear_history()
    # Save the history
    calculator.save_history()
    # Check that no error is raised and history remains empty
    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []

# Test history management negative cases

def test_history_exceeds_max_size(calculator):
    """Test that history does not exceed max size."""
    # Set max history size to 1 for testing
    calculator.config.max_history_size = 1
    # Perform an operation
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(5, 4)
    # Perform another operation
    calculator.perform_operation(3, 2)
    # Check that the history only contains one entry
    assert len(calculator.history) == 1


    






    




