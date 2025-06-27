###################################
# Operations file for the application
###################################

""""


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
        
        :param a: First number
        :param b: Second number
        :return: Result of the operation
        """
        pass

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        




        pass


    def __str__(self) -> str:        
        """
        String representation of the operation.
        
        :return: Name of the operation
        """
        return self.__class__.__name__
    


class Addition(Operation):



    

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

    def validate_operands(self, a, b):



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
    

class power(Operation):

    def validate_operands(self, a, b):
        
        
        
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

    def validate_operands(self, a, b):
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

    def validate_operands(self, a, b):
        
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

    def validate_operands(self, a, b):
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
    """ class for percentage operation.
    
    """
        
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Execute the percentage operation.
        
        :param a: Base number
        :param b: Percentage value
        :return: Result of the percentage operation
        """
        self.validate_operands(a, b)
        return (a * b) / 100

   

    
