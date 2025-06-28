###########################
# tests for calculation.py
###########################

"""

"""

import pytest
from decimal import Decimal
from datetime import datetime
from app.calculation import Calculation
from app.exceptions import OperationError
import logging

######################
# Test Cases for Calculation.calculate
######################

def test_calculate_addition():
    calc = Calculation(operation='add', operand1=Decimal('5.0'), operand2=Decimal('3.0'))
    assert calc.result == Decimal('8.0')

def test_calculate_subtraction():
    calc = Calculation(operation='subtract', operand1=Decimal('5.0'), operand2=Decimal('3.0'))
    assert calc.result == Decimal('2.0')

def test_calculate_multiplication():
    calc = Calculation(operation='multiply', operand1=Decimal('5.0'), operand2=Decimal('3.0'))
    assert calc.result == Decimal('15.0')

def test_calculate_division():
    calc = Calculation(operation='divide', operand1=Decimal('6.0'), operand2=Decimal('3.0'))
    assert calc.result == Decimal('2.0')

def test_calculate_division_by_zero():
    with pytest.raises(OperationError, match="Division by zero is not allowed."):
        Calculation(operation='divide', operand1=Decimal('5.0'), operand2=Decimal('0.0'))

def test_calculate_power():
    calc = Calculation(operation='power', operand1=Decimal('2.0'), operand2=Decimal('3.0'))
    assert calc.result == Decimal('8.0')

def test_calculate_power_negative_exponent():
    with pytest.raises(OperationError, match="Negative exponent is not allowed."):
        Calculation(operation='power', operand1=Decimal('2.0'), operand2=Decimal('-3.0'))


def test_calculate_root():
    calc = Calculation(operation='root', operand1=Decimal('9.0'), operand2=Decimal('2.0'))
    assert calc.result == Decimal('3.0')

def test_calculate_root_negative_operand():
    with pytest.raises(OperationError, match="Cannot calculate the root of a negative number."):
        Calculation(operation='root', operand1=Decimal('-9.0'), operand2=Decimal('2.0'))

def test_calculate_root_zero_exponent():
    with pytest.raises(OperationError, match="Root degree must be greater than zero."):
        Calculation(operation='root', operand1=Decimal('9.0'), operand2=Decimal('0.0'))

def test_calculate_modulus():
    calc = Calculation(operation='modulus', operand1=Decimal('5.0'), operand2=Decimal('3.0'))
    assert calc.result == Decimal('2.0')

def test_calculate_modulus_by_zero():
    with pytest.raises(OperationError, match="Modulus by zero is not allowed."):
        Calculation(operation='modulus', operand1=Decimal('5.0'), operand2=Decimal('0.0'))

def test_calculate_integer_division():
    calc = Calculation(operation='integerdivide', operand1=Decimal('5.0'), operand2=Decimal('3.0'))
    assert calc.result == Decimal('1.0')

def test_calculate_integer_division_by_zero():
    with pytest.raises(OperationError, match="Integer division by zero is not allowed."):
        Calculation(operation='integerdivide', operand1=Decimal('5.0'), operand2=Decimal('0.0'))

def test_calculate_percentage():
    calc = Calculation(operation='percentage', operand1=Decimal('200.0'), operand2=Decimal('50.0'))
    assert calc.result == Decimal('400.0')

def test_calculate_percentage_by_zero():
    with pytest.raises(OperationError, match="Cannot calculate percentage with zero base value."):
        Calculation(operation='percentage', operand1=Decimal('200.0'), operand2=Decimal('0.0'))

def test_calculate_absolute_difference():
    calc = Calculation(operation='absolutedifference', operand1=Decimal('5.0'), operand2=Decimal('3.0'))
    assert calc.result == Decimal('2.0')

def test_calculate_unknown_operation():
    with pytest.raises(OperationError, match="Unknown operation: invalid_operation"):
        Calculation(operation='invalid_operation', operand1=Decimal('5.0'), operand2=Decimal('3.0'))

def test_calculation_failed_exception():
    """Test that calculation failures are properly handled with OperationError."""
    # This test aims to trigger the exception handling of calculation.py
    # by creating a scenario that causes an InvalidOperation, ValueError, or ArithmeticError
    
    # Test with extremely large numbers that could cause overflow/calculation errors
    with pytest.raises(OperationError, match="Calculation failed"):
        # Using very large Decimal numbers that might cause issues in pow() conversion
        calc = Calculation(
            operation="power", 
            operand1=Decimal('1e308'), 
            operand2=Decimal('1e308')
        )


def test_to_dict():
    calc = Calculation(operation="add", operand1=Decimal("2"), operand2=Decimal("3"))
    result_dict = calc.to_dict()
    assert result_dict == {
        "operation": "add",
        "operand1": "2",
        "operand2": "3",
        "result": "5",
        "timestamp": calc.timestamp.isoformat()
    }

def test_from_dict():
    data = {
        "operation": "add",
        "operand1": "2",
        "operand2": "3",
        "result": "5",
        "timestamp": datetime.now().isoformat()
    }
    calc = Calculation.from_dict(data)
    assert calc.operation == "add"
    assert calc.operand1 == Decimal("2")
    assert calc.operand2 == Decimal("3")
    assert calc.result == Decimal("5")


def test_invalid_from_dict():
    data = {
        "operation": "add",
        "operand1": "invalid",
        "operand2": "3",
        "result": "5",
        "timestamp": datetime.now().isoformat()
    }
    with pytest.raises(OperationError, match="Invalid calculation data"):
        Calculation.from_dict(data)



def test_calculation_str():
    calc = Calculation(operation="add", operand1=Decimal("2"), operand2=Decimal("3"))
    assert str(calc) == "add(2, 3) = 5"

def test_repr_representation():
    """Test the __repr__ method of Calculation class."""
    calc = Calculation(operation="add", operand1=Decimal("2"), operand2=Decimal("3"))
    expected_repr = f"Calculation(operation='add', operand1=2, operand2=3, result=5, timestamp='{calc.timestamp.isoformat()}')"
    assert repr(calc) == expected_repr


def test_equality():
    calc1 = Calculation(operation="add", operand1=Decimal("2"), operand2=Decimal("3"))
    calc2 = Calculation(operation="add", operand1=Decimal("2"), operand2=Decimal("3"))
    calc3 = Calculation(operation="subtract", operand1=Decimal("5"), operand2=Decimal("3"))
    assert calc1 == calc2
    assert calc1 != calc3

def test_equality_with_non_calculation_object():
    """Test equality comparison with non-Calculation objects (covers line 283)."""
    calc = Calculation(operation="add", operand1=Decimal("2"), operand2=Decimal("3"))
    
    # Test comparison with different types of objects
    assert calc != "not a calculation"
    assert calc != 42
    assert calc != {"operation": "add", "operand1": 2, "operand2": 3}
    assert calc != [1, 2, 3]


def test_format_result():
    calc = Calculation(operation="divide", operand1=Decimal("1"), operand2=Decimal("3"))
    assert calc.format_result(precision=2) == "0.33"
    assert calc.format_result(precision=10) == "0.3333333333"
    assert calc.format_result(precision=0) == "0"







