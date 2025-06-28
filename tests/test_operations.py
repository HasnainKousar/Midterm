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


class TestRoot(BaseOperationTest):
    """ Test Root operation"""

    operation_class = Root
    valid_test_cases = {
        "square_root": {"a": 9, "b": 2, "expected": 3},
        "cube_root": {"a": 27, "b": 3, "expected": 3},
        "fourth_root": {"a": 16, "b": 4, "expected": 2},
        "decimal_base": {"a": 2.25, "b": 2, "expected": 1.5},
    }

    invalid_test_cases = {
        "negative_base": {
            "a": -9,
            "b": 2,
            "error": ValidationError,
            "message": "Cannot calculate the root of a negative number."  # Match actual error message
        },
        "zero_degree": {
            "a": 16,
            "b": 0,
            "error": ValidationError,
            "message": "Root degree must be greater than zero."  # Match actual error message
        },
        "negative_degree": {
            "a": 16,
            "b": -2,
            "error": ValidationError,
            "message": "Root degree must be greater than zero."  # Match actual error message
        }
    }


class TestPower(BaseOperationTest):
    """ Test Power operation"""

    operation_class = Power
    valid_test_cases = {
        "positive_base_and_exponent": {"a": 2, "b": 3, "expected": 8},
        "zero_exponent": {"a": 5, "b": 0, "expected": 1},
        "one_exponent": {"a": 5, "b": 1, "expected": 5},
        "decimal_base": {"a": 2.5, "b": 2, "expected": 6.25},
        "zero_base": {"a": 0, "b": 5, "expected": 0},
    }
    invalid_test_cases = {
        "negative_exponent": {
            "a": 2,
            "b": -3,
            "error": ValidationError,
            "message": "Negative exponent is not allowed for this operation."  # Match actual error message
        }
    }


class TestModulus(BaseOperationTest):
    """ Test Modulus operation"""

    operation_class = Modulus
    valid_test_cases = {
        "positive_integers": {"a": 5, "b": 3, "expected": 2},
        "negative_integers": {"a": -5, "b": -3, "expected": -2},
        "mixed_integers": {"a": 5, "b": -3, "expected": 2},
        "decimal_numbers": {"a": 5.5, "b": 3.2, "expected": 2.3},
        "zero_dividend": {"a": 0, "b": 1, "expected": 0},
        "large_numbers": {"a": 1e10, "b": 1e10, "expected": 0},
    }

    invalid_test_cases = {
        "zero_divisor": {
            "a": 5,
            "b": 0,
            "error": ValidationError,
            "message": "Modulus by zero is not allowed."
        }
    }


class TestIntegerDivision(BaseOperationTest):
    """ Test Integer Division operation"""

    operation_class = IntegerDivision
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
            "message": "Integer division by zero is not allowed."
        }
    }


class TestPercentage(BaseOperationTest):
    """ Test Percentage operation"""

    operation_class = Percentage
    valid_test_cases = {
        "quarter_percentage": {"a": 25, "b": 100, "expected": 25},  # 25 is 25% of 100
        "half_percentage": {"a": 50, "b": 100, "expected": 50},     # 50 is 50% of 100
        "decimal_numbers": {"a": 12.5, "b": 50, "expected": 25},    # 12.5 is 25% of 50
        "zero_numerator": {"a": 0, "b": 100, "expected": 0},        # 0 is 0% of 100
    }

    invalid_test_cases = {
        "zero_base": {
            "a": 25,
            "b": 0,
            "error": ValidationError,
            "message": "Cannot calculate percentage with zero base value."
        }
    }


class TestAbsoluteDifference(BaseOperationTest):
    """ Test Absolute Difference operation"""

    operation_class = AbsoluteDifference
    valid_test_cases = {
        "positive_integers": {"a": 5, "b": 3, "expected": 2},
        "negative_integers": {"a": -5, "b": -3, "expected": 2},
        "mixed_integers": {"a": 5, "b": -3, "expected": 8},
        "decimal_numbers": {"a": 5.5, "b": 3.2, "expected": 2.3},
        "zero_values": {"a": 0, "b": 0, "expected": 0},
    }

    invalid_test_cases = {} # No invalid cases for absolute difference


class TestOperationFactory:
    """
    Test class for OperationFactory.
    
   
    """

    def test_create_valid_operation(self):
        """Test creating a valid operation."""
        operation_map = {
            "add": Addition,
            "subtract": Subtraction,
            "multiply": Multiplication,
            "divide": Division,
            "power": Power,
            "root": Root,
            "modulus": Modulus,
            "integerdivide": IntegerDivision,
            "percentage": Percentage,
            "absolute": AbsoluteDifference
        }

        for op_name, op_class in operation_map.items():
            operation = OperationFactory.create_operation(op_name)
            assert isinstance(operation, op_class)

    def test_create_invalid_operation(self):
        """Test creating an invalid operation."""
        with pytest.raises(ValueError, match="Unknown operation type: invalid_operation"):
            OperationFactory.create_operation("invalid_operation")


    def test_register_operation(self):
        """Test registering a new operation."""
        class NewOperation(Operation):
            def execute(self, a: Decimal, b: Decimal) -> Decimal:
                return a + b
            
        OperationFactory.register_operation("new_op", NewOperation)
        operation = OperationFactory.create_operation("new_op")
        assert isinstance(operation, NewOperation)

    def test_register_invalid_operation(self):
        """Test registering an invalid operation class."""
        class NotAnOperation:
            pass

        with pytest.raises(TypeError, match="operation_class must be a subclass of Operation"):
            OperationFactory.register_operation("invalid_op", NotAnOperation)

