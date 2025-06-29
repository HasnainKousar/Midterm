#######################
# Advanced Calculator REPL
#######################

"""
THis module provides an advanced REPL (Read-Eval-Print Loop) for the calculator application.
It allows users to interactively perform calculations, manage history, and utilize advanced features like undo/
redo functionality.

"""

from decimal import Decimal
import logging

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory


def start_calculator_repl():
    """
    

    """


