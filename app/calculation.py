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
            "add": lambda a, b: a + b,
            "subtract": lambda a, b: a - b,
            "multiply": lambda a, b: a * b,
            "divide": lambda a, b: a /b if b != 0 else self._raise_div_zero(),
            "power": lambda a, b: (
                Decimal(pow(float(a), float(b))) if b >= 0 else self._raise_neg_power()
            ),
            "root": lambda a, b: (
                Decimal(pow(float(a), 1 / float(b)))
                if a >= 0 and b > 0
                else self._raise_invalid_root(a, b)
            ),
            "modulus": lambda a, b: a % b if b != 0 else self._raise_mod_zero(),
            "integerdivide": lambda a, b: a // b if b != 0 else self._raise_int_div_zero(),
            "percentage": lambda a, b: (a/ b) * 100 if b != 0 else self._raise_percent_zero(),
            "absolute": lambda a, b: abs(a - b)
        }

        op = operations.get(self.operation)
        if not op:
            raise OperationError(f"Unknown operation: {self.operation}")
        
        try:
            # execute the operation and return the result
            return op(self.operand1, self.operand2)
        except (InvalidOperation, ValueError, ArithmeticError) as e:
            raise OperationError(f"Calculation failed: {str(e)}")
        
    @staticmethod
    def _raise_div_zero():
        """
        Raise an OperationError for division by zero.
        
        This method is called when a division by zero is attempted.
        
        raises:
            OperationError: Indicating that division by zero is not allowed.
        """
        raise OperationError("Division by zero is not allowed.")
    
    @staticmethod
    def _raise_neg_power():
        """
        Raise an OperationError for negative power.
        
        This method is called when a negative power operation is attempted.
        
        raises:
            OperationError: Indicating that negative exponent is not allowed for this operation.
        """
        raise OperationError("Negative exponent is not allowed for this operation.")
    
    @staticmethod
    def _raise_invalid_root(a: Decimal, b: Decimal):
        """
        Raise an OperationError for invalid root operations.
        
        This method is called when an invalid root operation is attempted,
        such as negative base or invalid degree.
        
        raises:
            OperationError: Indicating the specific root validation error.
        """
        if a < 0:
            raise OperationError("Cannot calculate the root of a negative number.")
        
        if b <= 0:
            raise OperationError("Root degree must be greater than zero.")
        
        raise OperationError("Invalid root operation.")
    
    @staticmethod
    def _raise_mod_zero():
        """
        Raise an OperationError for modulus by zero.
        
        This method is called when a modulus operation with zero is attempted.
        
        raises:
            OperationError: Indicating that modulus by zero is not allowed.
        """
        raise OperationError("Modulus by zero is not allowed.")
    

    @staticmethod
    def _raise_int_div_zero():
        """
        Raise an OperationError for integer division by zero.
        
        This method is called when an integer division by zero is attempted.
        
        raises:
            OperationError: Indicating that integer division by zero is not allowed.
        """
        raise OperationError("Integer division by zero is not allowed.")
    
    @staticmethod
    def _raise_percent_zero():
        """
        Raise an OperationError for percentage calculation with zero base value.
        
        This method is called when a percentage calculation with a zero base value is attempted.
        
        raises:
            OperationError: Indicating that percentage calculation with zero base value is not allowed.
        """
        raise OperationError("Cannot calculate percentage with zero base value.")
    

    def to_dict(self) -> Dict[str, Any]:
        """ 
        Serialize the Calculation instance to a dictionary.

        This method converts the Calculation instance into a dictionary format,
        which can be useful for storage, transmission, or persistence.

        Returns:
            Dict[str, Any]: A dictionary representation of the Calculation instance.
        """
        return {
            "operation": self.operation,
            "operand1": str(self.operand1),
            "operand2": str(self.operand2),
            "result": str(self.result),
            "timestamp": self.timestamp.isoformat(),
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Calculation":
        """
        Deserialize a dictionary to create a Calculation instance.

        This method reconstructs a Calculation instance from a dictionary,
        which is useful for loading previously stored calculations. The result
        is recalculated and verified against the saved result for data integrity.

        Args:
            data (Dict[str, Any]): A dictionary containing the calculation data
                with keys: 'operation', 'operand1', 'operand2', 'result', 'timestamp'.

        Returns:
            Calculation: A new Calculation instance created from the provided dictionary.
        
        Raises:
            OperationError: If the data is invalid or missing required fields.
        """
        try:
            # Create the calculation object with the original operands
            calc = Calculation(
                operation=data['operation'],
                operand1=Decimal(data['operand1']),
                operand2=Decimal(data['operand2'])
            )

            # Set the timestamp from the saved data
            calc.timestamp = datetime.datetime.fromisoformat(data['timestamp'])

            # Verify the result matches (helps catch data corruption)
            saved_result = Decimal(data['result'])
            if calc.result != saved_result:
                logging.warning(
                    f"Loaded calculation result {saved_result} "
                    f"differs from computed result {calc.result}"
                )  # pragma: no cover

            return calc

        except (KeyError, InvalidOperation, ValueError) as e:
            raise OperationError(f"Invalid calculation data: {str(e)}")
        


    

