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
from operator import le
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

# Define type aliases for better readability
Number = Union[int, float, Decimal]
CalculationResult = Union[Decimal, str]


class Calculator:
    """
    
    """
    def __init__(self, config: Optional[CalculatorConfig] = None):
        """
        """
        # if no config is provided, create a default one
        if config is None:
            current_file = Path(__file__)
            project_root = current_file.parent.parent
            config = CalculatorConfig(base_dir=project_root)
        
        # Assign the configuration and validate it
        self.config = config
        self.config.validate()

        # make sure that log directory exists
        os.makedirs(self.config.log_dir, exist_ok=True)

        # set up logging system
        self._setup_logging()

        # initialize history and operation strategy
        self.history: List[Calculation] = []  # List to store Calculation history
        self.operation_strategy: Optional[Operation] = None  # Current operation strategy

        # initialize observers
        self.observers: List[HistoryObserver] = []

        # initialize stacks for undo/redo functionality
        self.undo_stack: List[CalculatorMemento] = []
        self.redo_stack: List[CalculatorMemento] = []

        # create required directories for history management
        self._setup_directories()

        try: 
            # load history from file if it exists
            self.load_history()
        except Exception as e: 
            # log the error if history loading fails
            logging.warning(f"Failed to load existing history: {e}")

        # log the initialization of the calculator
        logging.info("Calculator initialized with configuration")

    
    def _setup_logging(self):
        """
        
        """

        try:
            # make sure that log directory exists
            os.makedirs(self.config.log_dir, exist_ok=True)
            log_file = self.config.log_file.resolve()

            logging.basicConfig(
                filename = str(log_file),
                level = logging.INFO,
                format = '%(asctime)s - %(levelname)s - %(message)s',
                force= True  # Force reconfiguration of logging
            )
            logging.info(f'logging initialized at {log_file}')
        except Exception as e:
            print(f'Failed to set up logging: {e}')
            raise

    def _setup_directories(self) -> None:
        """

        """
        self.config.history_dir.mkdir(parents=True, exist_ok=True)


    









