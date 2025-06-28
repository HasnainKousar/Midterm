#####################################
# Calculation Module
#####################################  


from dataclasses import dataclass, field
import datetime
from decimal import Decimal, InvalidOperation
import logging
from typing import Any, Dict



from app.exceptions import OperationError


@dataclass
class Calculation:
    """
    
    
    """

    #required fields
    operation: str
    operand1: Decimal
    operand2: Decimal

    #fields with default values
    result: Decimal = field(init=False)
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

    def __post_init__(self):
        """
        Post-initialization processing to validate and perform the calculation.
        
        This method is called automatically after the dataclass is initialized.
        It validates the operation and performs the calculation, storing the result.
        """
       
        self.result = self.calculate()

    def calculate(self) -> Decimal:
        """
        Execute the calculation using the specified operation.
            
        utilizes a dictionary to map operation names to their corresponding lambda functions,
        enabling dynamic execution of the operation based on the operation name.
        
        returns:
            Decimal: The result of the calculation.
            
        raises:
            OperationError: If the operation is not recognized or if an error occurs during calculation.
        
        """
        operations = {
            "Addition": lambda a, b: a + b,
            "Subtraction": lambda a, b: a - b,
            "Multiplication": lambda a, b: a * b,
            "Division": lambda a, b: a /b if b != 0 else self._raise_div_zero(),
            "Power": lambda a, b: (
                Decimal(pow(float(a), float(b))) if b >= 0 else self._raise_neg_power()
            ),
            "Root": lambda a, b: (
                Decimal(pow(float(a), 1 / float(b))) if b > 0 else self._raise_neg_root()
            ),
            "Modulus": lambda a, b: a % b if b != 0 else self._raise_mod_zero(),
            "Integer Division": lambda a, b: a // b if b != 0 else self._raise_int_div_zero(),
            "Percentage": lambda a, b: (a/ b) * 100 if b != 0 else self._raise_percent_zero(),
            "Absolute Division": lambda a, b: abs(a - b)
        }

        op = operations.get(self.operation)
        if not op:
            raise OperationError(f"Unknown operation: {self.operation}")
        
        try:
            # execute the operation and return the result
            return op(self.operand1, self.operand2)
        except (InvalidOperation, ValueError, ArithmeticError) as e:
            raise OperationError(f"Calculation failed: {str(e)}")
        
