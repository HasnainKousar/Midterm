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

