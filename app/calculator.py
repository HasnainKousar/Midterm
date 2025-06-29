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
from tkinter import N
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

    def add_observer(self, observer: HistoryObserver) -> None:
        """
        
        """
        self.observers.append(observer)
        logging.info(f"Added observer: {observer.__class__.__name__}")


    def remove_observer(self, observer: HistoryObserver) -> None:
        """
        
        """
        self.observers.remove(observer)
        logging.info(f"Removed observer: {observer.__class__.__name__}")

    def notify_observers(self, calculation: Calculation) -> None:
        """
        
        """
        for observer in self.observers:
            observer.update(calculation)

    
    def set_operation(self, operation: Operation) -> None:
        """
        
        """

        self.operation_strategy = operation
        logging.info(f"Set operation: {operation}")

    
    def perform_operation(
            self,
            a: Union[str, Number],
            b: Union[str, Number]
    ) -> CalculationResult:
        """
        """
        if not self.operation_strategy:
            raise OperationError("No operation set. Please set an operation before performing calculations.")
        
        try:
             # validate and convert inputs to Decimal
            validate_a = InputValidator.validate_number(a, self.config)
            validate_b = InputValidator.validate_number(b, self.config)

            # excute the operation
            result = self.operation_strategy.execute(validate_a, validate_b)

            # Create a new Calculation object with the operation details
            calculation = Calculation(
                operation=str(self.operation_strategy),
                operand1=validate_a,
                operand2=validate_b,
            )

            # save the current state to the undo stack 
            self.undo_stack.append(CalculatorMemento(self.history.copy()))

            # clear the redo stack
            self.redo_stack.clear()

            # add the calculation to history
            self.history.append(calculation)

            # ensure history does not exceed max size
            if len(self.history) > self.config.max_history_size:
                self.history.pop(0)

            # notify observers about the new calculation
            self.notify_observers(calculation)

            return result
        
        except ValidationError as e:
            # log and re-raise validation errors
            logging.error(f"Validation error: {str(e)}")
            raise 
        except Exception as e:
            # log any other exceptions that occur during operation
            logging.error(f"Operation failed: {str(e)}")
            raise OperationError(f"Operation failed: {str(e)}")
        
    
    def save_history(self) -> None:
        """
        
        """

        try:
            # ensure history directory exists
            self.config.history_dir.mkdir(parents=True, exist_ok=True)

            history_data = []
            # prepare history data for saving
            for calc in self.history:
                history_data.append({
                    'operation': str(calc.operation),
                    'operand1': str(calc.operand1),
                    'operand2': str(calc.operand2),
                    'result': str(calc.result),
                    'timestamp': calc.timestamp.isoformat()
                })

            if history_data:
                # create a pandas DataFrame from the history data
                df = pd.DataFrame(history_data)
                # save the DataFrame to a CSV file
                df.to_csv(self.config.history_file, index=False)
                logging.info(f"History saved successfully to {self.config.history_file}")

            else:
                # if history is empty, create an empty CSV file with headers
                pd.DataFrame(columns=['operation', 'operand1', 'operand2', 'result', 'timestamp']).to_csv(
                    self.config.history_file, index=False
                )
                logging.info("Empty history saved to CSV file.")

        except Exception as e:
            # log any errors that occur during history saving
            logging.error(f"Failed to save history: {e}")
            raise OperationError(f"Failed to save history: {e}")
        
    def load_history(self) -> None:
        """
        
        """
        try:
            # check if history file exists
            if self.config.history_file.exists():
                # read the CSV file into a pandas DataFrame
                df = pd.read_csv(self.config.history_file)

                if not df.empty:
                    # Deserialize each row into a Calculation object
                    self.history = [
                        Calculation.from_dict({
                            'operation': row['operation'],
                            'operand1': row['operand1'],
                            'operand2': row['operand2'],
                            'result': row['result'],
                            'timestamp': row['timestamp']
                        })
                        for _, row in df.iterrows()
                    ]
                    logging.info(f"Loaded {len(self.history)} calculations from history file.")
                else:
                    logging.info("Loaded empty history file, no calculations found.")
            else:
                # if the history file does not exist, start with an empty history
                logging.info("History file does not exist, starting with empty history.")

        except Exception as e:
            # log any errors that occur during history loading
            logging.error(f"Failed to load history: {e}")
            raise OperationError(f"Failed to load history: {e}")
        

        

    
    
    
    









