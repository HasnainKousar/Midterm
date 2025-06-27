###################################
# Operations file for the application
###################################

"""
This module defines various mathematical operations as classes.
Each operation class inherits from the abstract base class `Operation`.
It includes methods for executing the operation and validating operands.

We will implement the following operations:
- Addition
- Subtraction
- Multiplication
- Division
- Power
- Root
- Modulus
- Integer Division
- Percentage
- Absolute Difference

we will use the factory pattern to create instances of these operations.

"""

from abc import ABC, abstractmethod
from typing import Dict
from decimal import Decimal
from app.exceptions import ValidationError


class Operation(ABC):
    """
    Abstract base class for operations.
    """

    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Execute the operation with two decimal numbers.
        
        Perform the operation defined by the subclass on the two operands.

        Args: 
            a (Decimal): First operand.
            b (Decimal): Second operand.

        Returns:
            Decimal: Result of the operation.
        """
        pass

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate the operands for the operation.

        This method checks if the operands are valid for the operation.
        It can be overridden by subclasses to implement specific validation rules.

        Args:
            a (Decimal): First operand.
            b (Decimal): Second operand.


        Raises:
            ValidationError: If the operands are not valid for the operation.
        
        """
        pass


    def __str__(self) -> str:        
        """
        String representation of the operation.
        
        :return: Name of the operation
        """
        return self.__class__.__name__
    


class Addition(Operation):
    """
    Class for addition operation.
    
    Performs addition of two decimal numbers.
    """
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Execute the addition operation.
        
        :param a: First number
        :param b: Second number
        :return: Result of the addition
        """
        self.validate_operands(a, b)
        return a + b
    

class Subtraction(Operation):
    """
    Class for subtraction operation.

    Performs subtraction of two decimal numbers.
    """

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Execute the subtraction operation.
        
        :param a: First number
        :param b: Second number
        :return: Result of the subtraction
        """
        self.validate_operands(a, b)
        return a - b
    


class Multiplication(Operation):
    """
    Class for multiplication operation.


    Performs multiplication of two decimal numbers.
    """

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Execute the multiplication operation.
        
        :param a: First number
        :param b: Second number
        :return: Result of the multiplication
        """
        self.validate_operands(a, b)
        return a * b
    

class Division(Operation):
    """
    Class for division operation.

    Performs division of two decimal numbers.
    """

    def validate_operands(self, a, b):
        """
        Validate the operands for the division operation.
        This method checks if the second operand is zero, which would cause a division by zero error.
        
        We override the base class method to add specific validation for division.
        :param a: First number
        :param b: Second number
        :raises ValidationError: If the second operand is zero.
        """
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Division by zero is not allowed.")
        

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Execute the division operation.
        
        :param a: First number
        :param b: Second number
        :return: Result of the division
        """
        self.validate_operands(a, b)
        return a / b
    

class Power(Operation):
    """
    Class for power operation.

    Performs exponentiation of a base number raised to a power.
    """

    def validate_operands(self, a, b):
        """
        Validate the operands for the power operation.
        This method checks if the second operand (exponent) is negative, which is not allowed
        for this operation. 
        
        We override the base class method to add specific validation for power.
        :param a: Base number
        :param b: Exponent
        :raises ValidationError: If the exponent is negative.
        """
        super().validate_operands(a, b)

        if b < 0:
            raise ValidationError("Negative exponent is not allowed for this operation.")
        

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Execute the power operation.
        
        :param a: Base number
        :param b: Exponent
        :return: Result of the power operation
        """
        self.validate_operands(a, b)
        return Decimal(pow(float(a), float(b)))
    
class Root(Operation):
    """Class for root operation.

    Performs the calculation of the nth root of a number.
    """


    def validate_operands(self, a, b):
        """
        Validate the operands for the root operation.
        This method checks if the first operand (number) is negative and the second
        operand (degree) is less than or equal to zero, which is not allowed for this operation.

        We override the base class method to add specific validation for root.
        :param a: Number to find the root of
        :param b: Degree of the root
        :raises ValidationError: If the number is negative or the degree is less than or equal to zero.
        """

        super().validate_operands(a, b)
        if a < 0:
            raise ValidationError("Cannot calculate the root of a negative number.")
        if b <= 0:
            raise ValidationError("Root degree must be greater than zero.")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Execute the root operation.
        
        :param a: Number to find the root of
        :param b: Degree of the root
        :return: Result of the root operation
        """
        self.validate_operands(a, b)
        return Decimal(pow(float(a), 1 / float(b)))
    

class Modulus(Operation):
    """Class for modulus operation. 

    Performs the modulus operation, which returns the remainder of the division of two numbers.
    """

    def validate_operands(self, a, b):
        """
        Validate the operands for the modulus operation.
        This method checks if the second operand (modulus) is zero, which would cause a
        modulus by zero error.

        We override the base class method to add specific validation for modulus.
        :param a: First number  
        :param b: Second number (modulus)
        :raises ValidationError: If the second operand is zero.
        """
        
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Modulus by zero is not allowed.")
        
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Execute the modulus operation.
        
        :param a: First number
        :param b: Second number
        :return: Result of the modulus operation
        """
        self.validate_operands(a, b)
        return a % b
    
class IntegerDivision(Operation):
    """Class for integer division operation.

    Performs integer division of two decimal numbers, returning the quotient without the remainder.
    """

    def validate_operands(self, a, b):
        """
        Validate the operands for the integer division operation.
        This method checks if the second operand (divisor) is zero, which would cause a
        division by zero error, and if both operands are integers.  

        We override the base class method to add specific validation for integer division.
        :param a: First number (dividend)
        :param b: Second number (divisor)
        :raises ValidationError: If the second operand is zero or if either operand is not an integer.
        """


        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Integer division by zero is not allowed.")
        if not (a % 1 == 0 and b % 1 == 0):
            raise ValidationError("Both operands must be integers for integer division.")
        
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Execute the integer division operation.
        
        :param a: First number
        :param b: Second number
        :return: Result of the integer division operation
        """
        self.validate_operands(a, b)
        return a // b
    
class Percentage(Operation):
    """ Class for percentage operation.

    Performs the calculation of a percentage of a number.

    """

    def validate_operands(self, a, b):

        """
        Validate the operands for the percentage operation.
        This method checks if the second operand (percentage value) is zero, which would cause a
        division by zero error.

        We override the base class method to add specific validation for percentage.
        :param a: Base number
        :param b: Percentage value
        :raises ValidationError: If the second operand is zero.
        """
        
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Percentage value cannot be zero.")
        
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Execute the percentage operation.
        
        :param a: Base number
        :param b: Percentage value
        :return: Result of the percentage operation
        """
        self.validate_operands(a, b)
        return (a/ b) * 100 




class AbsoluteDifference(Operation):
    """ Class for absolute difference operation.

    Performs the calculation of the absolute difference between two numbers.
    """
    
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Execute the absolute difference operation.
        
        :param a: First number
        :param b: Second number
        :return: Result of the absolute difference operation
        """
        self.validate_operands(a, b)
        return abs(a - b)
    




class OperationFactory:
    """
    Factory class to create operation instances.

    This class provides a way to create instances of various mathematical operations
    based on the operation type. It uses a dictionary to map operation names to their
    corresponding classes. New operations can be registered dynamically.

    Attributes:
        _operations (Dict[str, type]): A dictionary mapping operation names to their classes.

    """

    _operations: Dict[str, type] = {
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

    @classmethod
    def register_operation(cls, name: str, operation_class: type) -> None:
        """
        Register a new operation class with a name.

        args:
            name (str): the name of the operation (e.g., "add", "subtract", etc.).
            operation_class (type): the class implementing the operation, which must be a subclass of Operation

        Raises:
            TypeError: If the operation_class is not a subclass of Operation.

        """


        if not issubclass(operation_class, Operation):
            raise TypeError("Operation class must be a subclass of Operation.")
        cls._operations[name.lower()] = operation_class


    @classmethod
    def create_operation(cls, operation_type: str) -> Operation:
        """
        Create an instance of the specified operation type.

        This method retrieves the operation class from the _operation dictionary
        and creates an instance of it.

        Args:
            operation_type (str): The type of operation to create (e.g., "add",
            "subtract", "multiply", etc.).

        Returns:
            Operation: An instance of the specified operation class.

        Raises:
            ValueError: If the operation type is not recognized.
        """

        operation_class = cls._operations.get(operation_type.lower())
        if not operation_class:
            raise ValueError(f"Unkown operation type: {operation_type}")
        return operation_class()
    





    
