#############################
# Tests for the Calculator REPL
#############################

"""

"""

from unittest import mock
import pytest
from unittest.mock import Mock, patch
from app.calculator_repl import start_calculator_repl
from app.exceptions import OperationError, ValidationError


#Test case for exitting the REPL with a valid command
@patch('builtins.input', side_effect=['exit'])
@patch('builtins.print')
def test_run_calculator_repl_exit(mock_print, mock_input):
    with patch('app.calculator.Calculator.save_history') as mock_save_history:
        start_calculator_repl()
        mock_save_history.assert_called_once()
        mock_print.assert_any_call("History saved successfully.")
        mock_print.assert_any_call("Exiting calculator REPL. Goodbye!")



# Test case for displaying help in the REPL
@patch('builtins.input', side_effect=['help', 'exit'])
@patch('builtins.print')
def test_run_calculator_repl_help(mock_print, mock_input):
    """Test REPL help command."""
    with patch('app.calculator.Calculator.save_history') as mock_save_history:
        start_calculator_repl()
        mock_save_history.assert_called_once()  # save_history is called during exit
        mock_print.assert_any_call("\nAvailable commands:")
        mock_print.assert_any_call("  add, subtract, multiply, divide, power, root, modulus, integerdivision, percentage, absolutedifference")
        mock_print.assert_any_call("  exit - Exit the calculator REPL")

@patch('builtins.input', side_effect=['add', '2', '3', 'history', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_run_calculator_repl_history_with_calculations(mock_calculator_class, mock_print, mock_input):
    """Test REPL history command with calculations in history"""
    # Create a mock calculator instance
    mock_calc = Mock()
    # Mock the show_history to return some calculations when called
    mock_calc.show_history.return_value = [
        "Addition(2, 3) = 5"]
    mock_calc.add_observer = Mock()
    mock_calc.set_operation = Mock()
    mock_calc.perform_calculation.side_effect = [5, 20]  # Return values for calculations
    mock_calculator_class.return_value = mock_calc
    
    start_calculator_repl()
    
    # Verify save_history was called on exit
    mock_calc.save_history.assert_called()
    # Verify the correct messages for history with calculations
    mock_print.assert_any_call("\nCalculation History:")
    mock_print.assert_any_call("1. Addition(2, 3) = 5")
    





