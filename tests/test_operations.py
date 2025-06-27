###########################
#Test for operations module
###########################

import pytest
from decimal import Decimal
from typing import Any, Dict, Type

from app.operations import (
    Operation,
    Addition,
    Subtraction,
    Multiplication,
    Division,
    Root,
    Power,
    Modulus,
    IntegerDivision,
    AbsoluteDifference,
    Percentage,
    OperationFactory,
)

from app.exceptions import ValidationError


class TestOperation:
    """ Test base Operation class functionality """

    def test_str_repr(self):
        """ Test string representation of Operation """
        class TestOP(Operation):
            def execute(self, a: Decimal, b: Decimal) -> Decimal:
                return a
            
        assert str(TestOP()) == "TestOP"  # str representation should be class name

class BaseOperationTest:
    """ A base operation for testing purposes """
    
    operation_class: Type[Operation]
    valid_test_cases: Dict[str, Any]
    invalid_test_cases: Dict[str, Any]

    def test_valid_operations(self):
        """ Test valid operations """
        
        operation = self.operation_class()
        for name, case in self.valid_test_cases.items():
            a = Decimal(str(case['a']))
            b = Decimal(str(case['b']))
            expected = Decimal(str(case['expected']))
            result = operation.execute(a, b)
            assert result == expected, f"Failed for {name}"


    def test_invalid_operations(self):
        """ Test invalid operations """
        
        operation = self.operation_class()
        for name, case in self.invalid_test_cases.items():
            a = Decimal(str(case['a']))
            b = Decimal(str(case['b']))
            error = case.get('error', ValidationError)
            error_message = case.get('message', "")

            with pytest.raises(error, match=error_message):
                operation.execute(a, b)


class TestAddition(BaseOperationTest):
    """ Test Addition operation"""

    operation_class = Addition
    valid_test_cases = {
        "positive_integers": {"a": 5, "b": 3, "expected": 8},
        "negative_integers": {"a": -5, "b": -3, "expected": -8},
        "mixed_integers": {"a": 5, "b": -3, "expected": 2},
        "decimal_numbers": {"a": 5.5, "b": 3.2, "expected": 8.7},
        "zero": {"a": 0, "b": 0, "expected": 0},
        "large_numbers": {"a": 1e10, "b": 1e10, "expected": 2e10},
    }

    invalid_test_cases = {} # No invalid cases for addition


class TestSubtraction(BaseOperationTest):
    """ Test Subtraction operation"""

    operation_class = Subtraction
    valid_test_cases = {
        "positive_integers": {"a": 5, "b": 3, "expected": 2},
        "negative_integers": {"a": -5, "b": -3, "expected": -2},
        "mixed_integers": {"a": 5, "b": -3, "expected": 8},
        "decimal_numbers": {"a": 5.5, "b": 3.2, "expected": 2.3},
        "zero": {"a": 0, "b": 0, "expected": 0},
        "large_numbers": {"a": 1e10, "b": 1e10, "expected": 0},
    }

    invalid_test_cases = {} # No invalid cases for subtraction



class TestMultiplication(BaseOperationTest):
    """ Test Multiplication operation"""

    operation_class = Multiplication
    valid_test_cases = {
        "positive_integers": {"a": 5, "b": 3, "expected": 15},
        "negative_integers": {"a": -5, "b": -3, "expected": 15},
        "mixed_integers": {"a": 5, "b": -3, "expected": -15},
        "decimal_numbers": {"a": 5.5, "b": 3.2, "expected": 17.6},
        "zero": {"a": 0, "b": 0, "expected": 0},
        "large_numbers": {"a": 1e10, "b": 1e10, "expected": 1e20},
    }

    invalid_test_cases = {} # No invalid cases for multiplication


class TestDivision(BaseOperationTest):
    """ Test Division operation"""

    operation_class = Division
    valid_test_cases = {
        "positive_integers": {"a": 6, "b": 3, "expected": 2},
        "negative_integers": {"a": -6, "b": -3, "expected": 2},
        "mixed_integers": {"a": 6, "b": -3, "expected": -2},
        "decimal_numbers": {"a": 6.0, "b": 3.0, "expected": 2.0},
        "zero_dividend": {"a": 0, "b": 1, "expected": 0},
        "large_numbers": {"a": 1e10, "b": 1e10, "expected": 1},
    }

    invalid_test_cases = {
        "zero_divisor": {
            "a": 5,
            "b": 0,
            "error": ValidationError,
            "message": "Division by zero is not allowed."
        }
    }






 

