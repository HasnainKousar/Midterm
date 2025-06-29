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

# Test for adding and removing observers
def test_add_observer(calculator):
    """ """
    observer = LoggingObserver()
    calculator.add_observer(observer)
    assert observer in calculator.observers

def test_remove_observer(calculator):
    """ """
    observer = LoggingObserver()
    calculator.add_observer(observer)
    calculator.remove_observer(observer)
    assert observer not in calculator.observers

# Test for performing operations
def test_perform_operation_addition(calculator):
    """Test for performing addition operation."""
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    result = calculator.perform_operation(5, 4)
    assert result == Decimal('9')

def test_perform_operation_validation_error(calculator):
    """ """
    calculator.set_operation(OperationFactory.create_operation('add'))
    with pytest.raises(ValidationError):
        calculator.perform_operation("five", 4)


def test_perform_operation_operation_error(calculator):
    """ """
    with pytest.raises(OperationError, match="No operation set. Please set an operation before performing calculations."):
        calculator.perform_operation(5, 4)




