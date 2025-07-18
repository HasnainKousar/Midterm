###########################
# test_validators.py
###########################

"""
Input Validation Tests Module

This module contains comprehensive unit tests for the InputValidator class,
which is responsible for validating and converting user input in the calculator application.

The tests cover:
- Positive test cases: Valid inputs (integers, decimals, strings)
- Negative test cases: Invalid inputs (non-numeric strings, exceeding limits, None values)
- Edge cases: Zero values, whitespace handling, boundary conditions
"""
from logging import config
import pytest
from decimal import Decimal
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError
from app.input_validators import InputValidator

# sample configuration for testing with max input value of 100,000
config = CalculatorConfig(max_input_value=Decimal('100000'))


############################
# Positive Test Cases
############################
def test_validate_number_positive_integer():
    """Test validation of a positive integer."""
    assert InputValidator.validate_number(42, config) == Decimal('42')

def test_validate_number_negative_integer():
    """Test validation of a negative integer."""
    assert InputValidator.validate_number(-18, config) == Decimal('-18')

def test_validate_positive_decimal():
    """Test validation of a positive decimal."""
    assert InputValidator.validate_number(Decimal('3.14'), config) == Decimal('3.14')

def test_validate_negative_decimal():
    """Test validation of a negative decimal."""
    assert InputValidator.validate_number(Decimal('-2.718'), config) == Decimal('-2.718')

def test_validate_number_positive_string():
    """Test validation of a positive number in string format."""
    assert InputValidator.validate_number('154', config) == Decimal('154')

def test_validate_number_postive_decimal_string():
    """Test validation of a positive decimal in string format."""
    assert InputValidator.validate_number('77.123', config) == Decimal('77.123')

def test_validate_number_negative_string():
    """Test validation of a negative number in string format."""
    assert InputValidator.validate_number('-42', config) == Decimal('-42')

def test_validate_number_negative_decimal_string():
    """Test validation of a negative decimal in string format."""
    assert InputValidator.validate_number('-3.14', config) == Decimal('-3.14')

def test_validate_number_zero():
    """Test validation of zero."""
    assert InputValidator.validate_number(0, config) == Decimal('0')

def test_validate_number_trimmed_string():
    """Test validation of a number with leading/trailing spaces."""
    assert InputValidator.validate_number('   245.231   ', config) == Decimal('245.231')

#############################
# Negative Test Cases
#############################

def test_validate_number_invalid_string():
    """Test validation of an invalid string."""
    with pytest.raises(ValidationError, match="Invalid number format: abc"):
        InputValidator.validate_number('abc', config)


def test_validate_number_exceeds_max_value():
    """Test validation of a number that exceeds the maximum allowed value."""
    with pytest.raises(ValidationError, match="Input exceeds maximum allowed value: 100000"):
        InputValidator.validate_number(Decimal('100001'), config)


def test_validate_number_empty_string():
    """Test validation of an empty string."""
    with pytest.raises(ValidationError, match="Invalid number format: "):
        InputValidator.validate_number('', config)

def test_validate_number_none():
    """Test validation of None input."""
    with pytest.raises(ValidationError, match="Invalid number format: None"):
        InputValidator.validate_number(None, config)

