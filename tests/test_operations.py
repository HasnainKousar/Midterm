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

class BaseOperation(Operation):
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

 

