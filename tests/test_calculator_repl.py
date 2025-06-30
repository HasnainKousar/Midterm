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
    
# Test case for exit command with an error during history saving
@patch('builtins.input', side_effect=['exit'])
@patch('builtins.print')
def test_run_calculator_repl_exit_with_error(mock_print, mock_input):
    """Test REPL exit command with an error during history saving."""
    with patch('app.calculator.Calculator.save_history') as mock_save_history:
        mock_save_history.side_effect = OperationError("Save failed")
        start_calculator_repl()
        mock_print.assert_any_call("Warning: Could not save history before exiting: Save failed")
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

# Test case for saving history in the REPL
@patch('builtins.input', side_effect=['add', '2', '3', 'save', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_run_calculator_repl_save_history(mock_calculator_class, mock_print, mock_input):
    """Test REPL save command"""
    # Create a mock calculator instance
    mock_calc = Mock()
    mock_calc.save_history = Mock()
    mock_calc.add_observer = Mock()
    mock_calculator_class.return_value = mock_calc

    start_calculator_repl()

    # Verify save_history was called (once for the save command and once on exit)
    assert mock_calc.save_history.call_count == 2
    # Verify the correct message for saving history
    mock_print.assert_any_call("History saved successfully.")

# Test case for saving history in the REPL with an error
@patch('builtins.input', side_effect=['save', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_run_calculator_repl_save_error(mock_calculator_class, mock_print, mock_input):
    """Test REPL save command when error occurs."""
    # Create a mock calculator instance
    mock_calc = Mock()
    mock_calc.add_observer = Mock()
    # Make save_history fail when called explicitly but succeed on exit
    call_count = 0
    def save_side_effect():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise Exception("Save failed")
        # Let subsequent calls (exit) succeed
        return None
    
    mock_calc.save_history.side_effect = save_side_effect
    mock_calculator_class.return_value = mock_calc
    
    start_calculator_repl()
    
    # Verify save_history was called
    assert mock_calc.save_history.call_count >= 1
    # Verify the correct error message
    mock_print.assert_any_call("Error saving history: Save failed")

# Test case for canceling the first number input in the REPL
@patch('builtins.input', side_effect=['add', 'cancel', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_run_calculator_repl_cancel_first_number(mock_calculator_class, mock_print, mock_input):
    """Test REPL canceling first number input."""
    # Create a mock calculator instance
    mock_calc = Mock()
    mock_calc.add_observer = Mock()
    mock_calculator_class.return_value = mock_calc
    
    start_calculator_repl()
    
    # Verify that no calculations were performed
    mock_calc.perform_calculation.assert_not_called()
    # Verify the correct message for operation cancellation
    mock_print.assert_any_call("Operation cancelled.")

# Test case for canceling the second number input in the REPL
@patch('builtins.input', side_effect=['add', '2', 'cancel', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_run_calculator_repl_cancel_second_number(mock_calculator_class, mock_print, mock_input):
    """Test REPL canceling second number input."""
    # Create a mock calculator instance
    mock_calc = Mock()
    mock_calc.add_observer = Mock()
    mock_calculator_class.return_value = mock_calc
    
    start_calculator_repl()
    
    # Verify that no calculations were performed
    mock_calc.perform_calculation.assert_not_called()
    # Verify the correct message for operation cancellation
    mock_print.assert_any_call("Operation cancelled.")

# Test case for normalizing results in the REPL
@patch('builtins.input', side_effect=['add', '2', '3', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_run_calculator_repl_normalize_result(mock_calculator_class, mock_print, mock_input):
    """Test REPL normalizing Decimal results."""
    from decimal import Decimal
    
    # Create a mock calculator instance
    mock_calc = Mock()
    mock_calc.add_observer = Mock()
    mock_calc.set_operation = Mock()
    
    # Create a Decimal result that needs normalization (e.g., 5.00 -> 5)
    decimal_result = Decimal('5.00')
    mock_calc.perform_operation.return_value = decimal_result
    mock_calculator_class.return_value = mock_calc
    
    start_calculator_repl()
    
    # Verify that the result was printed (normalized from 5.00 to 5)
    mock_print.assert_any_call("\nResult: 5")
    # Verify perform_operation was called
    mock_calc.perform_operation.assert_called_once()

###################################
# Test cases for handling errors in the REPL
###################################

# Test case for handling an OperationError performed operation
@patch('builtins.input', side_effect=['add', '2', '0', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_run_calculator_repl_operation_error(mock_calculator_class, mock_print, mock_input):
    """Test REPL handling OperationError during operation."""
    # Create a mock calculator instance
    mock_calc = Mock()
    mock_calc.add_observer = Mock()
    mock_calc.set_operation = Mock()
    # Simulate an OperationError for division by zero
    mock_calc.perform_operation.side_effect = OperationError("Division by zero is not allowed.")
    mock_calculator_class.return_value = mock_calc
    
    start_calculator_repl()
    
    # Verify that the error message was printed
    mock_print.assert_any_call("Error: Division by zero is not allowed.")
    
# Test case for handling a ValidationError during input validation
@patch('builtins.input', side_effect=['add', 'invalid', '3', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_run_calculator_repl_validation_error(mock_calculator_class, mock_print, mock_input):
    """Test REPL handling ValidationError during input validation."""
    # Create a mock calculator instance
    mock_calc = Mock()
    mock_calc.add_observer = Mock()
    mock_calc.set_operation = Mock()
    # Simulate a ValidationError for invalid input
    mock_calc.perform_operation.side_effect = ValidationError("Invalid input")
    mock_calculator_class.return_value = mock_calc
    
    start_calculator_repl()
    
    # Verify that the error message was printed
    mock_print.assert_any_call("Error: Invalid input")

# Test case for handling unexpected exceptions in the REPL
@patch('builtins.input', side_effect=['add', '2', '3', 'unexpected', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_run_calculator_repl_unexpected_error(mock_calculator_class, mock_print, mock_input):
    """Test REPL handling unexpected exceptions."""
    # Create a mock calculator instance
    mock_calc = Mock()
    mock_calc.add_observer = Mock()
    mock_calc.set_operation = Mock()
    # Simulate an unexpected exception
    mock_calc.perform_operation.side_effect = Exception("Unexpected error")
    mock_calculator_class.return_value = mock_calc
    
    start_calculator_repl()
    
    # Verify that the unexpected error message was printed
    mock_print.assert_any_call("An unexpected error occurred: Unexpected error")

# Test case for handling KeyboardInterrupt in the REPL
@patch('builtins.input', side_effect=KeyboardInterrupt())
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_run_calculator_repl_keyboard_interrupt(mock_calculator_class, mock_print, mock_input):
    """Test REPL KeyboardInterrupt handling."""
    # Create a mock calculator instance
    mock_calc = Mock()
    mock_calc.add_observer = Mock()
    mock_calculator_class.return_value = mock_calc
    
    # Mock input to raise KeyboardInterrupt first, then 'exit'
    with patch('builtins.input') as mock_input_patch:
        mock_input_patch.side_effect = [KeyboardInterrupt(), 'exit']
        start_calculator_repl()
    
    # Verify the correct message for KeyboardInterrupt
    mock_print.assert_any_call("\nOperation cancelled by user.")

# Test case for handling EOFError in the REPL
@patch('builtins.input', side_effect=EOFError())
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_run_calculator_repl_eof_error(mock_calculator_class, mock_print, mock_input):
    """Test REPL EOFError handling."""
    # Create a mock calculator instance
    mock_calc = Mock()
    mock_calc.add_observer = Mock()
    mock_calculator_class.return_value = mock_calc
    
    start_calculator_repl()
    
    # Verify the correct message for EOFError
    mock_print.assert_any_call("\nInput terminated by user. Exiting REPL....")

# Test case for other unexpected errors in the REPL
@patch('builtins.input', side_effect=RuntimeError("Command processing error"))
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_run_calculator_repl_general_exception(mock_calculator_class, mock_print, mock_input):
    """Test REPL general exception handling in main loop."""
    # Create a mock calculator instance
    mock_calc = Mock()
    mock_calc.add_observer = Mock()
    mock_calculator_class.return_value = mock_calc
    
    # Mock input to raise an exception first, then 'exit'
    with patch('builtins.input') as mock_input_patch:
        mock_input_patch.side_effect = [RuntimeError("Command processing error"), 'exit']
        start_calculator_repl()
    
    # Verify the correct message for general exception
    mock_print.assert_any_call("Error: Command processing error")

# Test case for handling unexpected errors during calculator startup
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_run_calculator_repl_initialization_error(mock_calculator_class, mock_print):
    """Test REPL initialization error handling."""
    # Simulate an error during calculator initialization
    mock_calculator_class.side_effect = Exception("Initialization failed")
    
    with pytest.raises(Exception, match="Initialization failed"):
        start_calculator_repl()
    
    # Verify the correct error message was printed
    mock_print.assert_any_call("Failed to start calculator REPL: Initialization failed")




