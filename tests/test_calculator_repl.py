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
