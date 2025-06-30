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

# Test case for performing a valid addition operation and history saving
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
    
# Test case for history command with no calculations in history
@patch('builtins.input', side_effect=['history', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_run_calculator_repl_history_with_no_calculations(mock_calculator_class, mock_print, mock_input):
    """Test REPL history command with no calculations in history"""
    # Create a mock calculator instance
    mock_calc = Mock()
    mock_calc.show_history.return_value = []  # Empty history
    mock_calc.add_observer = Mock()
    mock_calculator_class.return_value = mock_calc

    start_calculator_repl()

    # Verify save_history was called on exit
    mock_calc.save_history.assert_called()
    # Verify the correct message for no calculations in history
    mock_print.assert_any_call("No calculations performed yet.")

# Test case for clearing history in the REPL
@patch('builtins.input', side_effect=['add', '2', '3', 'clear', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_run_calculator_repl_clear_history(mock_calculator_class, mock_print, mock_input):
    """Test REPL clear command"""
    # Create a mock calculator instance
    mock_calc = Mock()
    mock_calc.clear_history = Mock()
    mock_calc.add_observer = Mock()
    mock_calculator_class.return_value = mock_calc

    start_calculator_repl()

    # Verify clear_history was called
    mock_calc.clear_history.assert_called_once()
    # Verify the correct message for clearing history
    mock_print.assert_any_call("History cleared.")

# Test case for undo command in the REPL
@patch('builtins.input', side_effect=['add', '2', '3', 'undo', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_run_calculator_repl_undo(mock_calculator_class, mock_print, mock_input):
    """Test REPL undo command"""
    # Create a mock calculator instance
    mock_calc = Mock()
    mock_calc.undo = Mock()
    mock_calc.add_observer = Mock()
    mock_calculator_class.return_value = mock_calc

    start_calculator_repl()

    # Verify undo was called
    mock_calc.undo.assert_called_once()
    # Verify the correct message for undoing the last operation
    mock_print.assert_any_call("Last operation undone.")

# Test case for undo command in the REPL with no operations to undo
@patch('builtins.input', side_effect=['undo', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_run_calculator_repl_undo_no_operations(mock_calculator_class, mock_print, mock_input):
    """Test REPL undo command with no operations to undo"""
    # Create a mock calculator instance
    mock_calc = Mock()
    mock_calc.add_observer = Mock()
    mock_calc.undo.return_value = False  # No operation to undo
    mock_calculator_class.return_value = mock_calc
    
    start_calculator_repl()
    
    # Verify undo was called
    mock_calc.undo.assert_called_once()
    # Verify the correct message for failed undo
    mock_print.assert_any_call("No operations to undo.")

# Test case for redo command in the REPL
@patch('builtins.input', side_effect=['add', '2', '3', 'undo', 'redo', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_run_calculator_repl_redo(mock_calculator_class, mock_print, mock_input):
    """Test REPL redo command"""
    # Create a mock calculator instance
    mock_calc = Mock()
    mock_calc.undo = Mock()
    # Mock redo to simulate redoing the last operation
    mock_calc.redo = Mock()
    mock_calc.add_observer = Mock()
    mock_calculator_class.return_value = mock_calc

    start_calculator_repl()
    # Verify undo was called
    mock_calc.undo.assert_called_once()
    # Verify redo was called
    mock_calc.redo.assert_called_once()
    # Verify the correct message for redoing the last operation
    mock_print.assert_any_call("Last operation redone.")



# Test case for redo command in the REPL with no operations to redo
@patch('builtins.input', side_effect=['redo', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_run_calculator_repl_redo_no_operations(mock_calculator_class, mock_print, mock_input):
    """Test REPL redo command with no operations to redo"""
    # Create a mock calculator instance
    mock_calc = Mock()
    mock_calc.add_observer = Mock()
    mock_calc.redo.return_value = False  # No operation to undo
    mock_calculator_class.return_value = mock_calc
    
    start_calculator_repl()
    
    # Verify undo was called
    mock_calc.redo.assert_called_once()
    # Verify the correct message for failed undo
    mock_print.assert_any_call("No operations to redo.")

# Test case for loading history in the REPL
@patch('builtins.input', side_effect=['load', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_run_calculator_repl_load_history(mock_calculator_class, mock_print, mock_input):
    """Test REPL load command"""
    # Create a mock calculator instance
    mock_calc = Mock()
    mock_calc.load_history = Mock()
    mock_calc.add_observer = Mock()
    mock_calculator_class.return_value = mock_calc

    start_calculator_repl()

    # Verify load_history was called
    mock_calc.load_history.assert_called_once()
    # Verify the correct message for loading history
    mock_print.assert_any_call("History loaded successfully.")

# Test case for loading history in the REPL with an error
@patch('builtins.input', side_effect=['load', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_run_calculator_repl_load_history_error(mock_calculator_class, mock_print, mock_input):
    """Test REPL load command with an error"""
    # Create a mock calculator instance
    mock_calc = Mock()
    mock_calc.load_history.side_effect = Exception("Load error")
    mock_calc.add_observer = Mock()
    mock_calculator_class.return_value = mock_calc

    start_calculator_repl()

    # Verify load_history was called
    mock_calc.load_history.assert_called_once()
    # Verify the correct message for loading history error
    mock_print.assert_any_call("Error loading history: Load error")


    





    



