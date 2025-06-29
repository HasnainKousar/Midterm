############################
# test_exceptions.py
############################

"""
Exception Handling Tests

This module tests the custom exception classes used throughout the calculator application.
It verifies that exceptions can be raised properly, have correct inheritance relationships,
and carry appropriate error messages. Tests cover CalculatorError (base), ValidationError,
OperationError, and ConfigurationError classes.
"""

import pytest
from app.exceptions import CalculatorError, ConfigurationError, OperationError, ValidationError


def test_calculator_error_is_base_exception():
    """Test that CalculatorError is the base exception for calculator-related errors."""
    with pytest.raises(CalculatorError) as exc_info:
        raise CalculatorError("Base calculator error occurred.")
    assert str(exc_info.value) == "Base calculator error occurred."


def test_validation_error_is_calculator_error():
    """Test that ValidationError can be raised as a CalculatorError."""
    with pytest.raises(CalculatorError) as exc_info:
        raise ValidationError("Validation failed")
    assert isinstance(exc_info.value, CalculatorError)
    assert str(exc_info.value) == "Validation failed"

def test_validation_error_specific_exception():
    """Test that ValidationError can be raised as a specific exception."""
    with pytest.raises(ValidationError) as exc_info:
        raise ValidationError("Validation error")
    assert str(exc_info.value) == "Validation error"

def test_operation_error_is_calculator_error():
    """Test that OperationError can be raised as a CalculatorError."""
    with pytest.raises(CalculatorError) as exc_info:
        raise OperationError("Operation failed")
    assert isinstance(exc_info.value, CalculatorError)
    assert str(exc_info.value) == "Operation failed"

def test_operation_error_specific_exception():
    """Test that OperationError can be raised as a specific exception."""
    with pytest.raises(OperationError) as exc_info:
        raise OperationError("Specific operation error")
    assert str(exc_info.value) == "Specific operation error"


def test_configuration_error_is_calculator_error():
    """Test that ConfigurationError can be raised as a CalculatorError."""
    with pytest.raises(CalculatorError) as exc_info:
        raise ConfigurationError("Configuration error")
    assert isinstance(exc_info.value, CalculatorError)
    assert str(exc_info.value) == "Configuration error"

def test_configuration_error_specific_exception():
    """Test that ConfigurationError can be raised as a specific exception."""
    with pytest.raises(ConfigurationError) as exc_info:
        raise ConfigurationError("Specific configuration error")
    assert str(exc_info.value) == "Specific configuration error"