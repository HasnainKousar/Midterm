############################
# calculator.py
############################

"""
In this we will implement the main Calculator class that integrates 
all components, manages operations, history, observers, and configuration.


Key Concepts:

-Integration of Design Patterns: The Calculator class will utilize the
 Memento, Observer, and Strategy patterns to manage its operations and history.

-Data Persistence with pandas and csv: The Calculator will save its history
 to a CSV file using pandas, allowing for easy data manipulation and retrieval.

-Logging: The Calculator will log operations and errors using the logging module,
 providing a clear audit trail of all calculations performed.


"""

from decimal import Decimal
import logging
import os
from pathlib import Path
from typing import List, Optional, Union, Any, Dict
import pandas as pd

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento
from app.exceptions import OperationError, ValidationError
from app.history import HistoryObserver
from app.input_validators import InputValidator
from app.operations import Operation

