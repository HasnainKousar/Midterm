###########################
# History management for the application
###########################

"""
History Management Module

This module implements the Observer pattern for managing calculation history in the calculator application.
It provides a flexible system for tracking, logging, and automatically saving calculation events.

The module contains:
- HistoryObserver: Abstract base class defining the observer interface
- LoggingObserver: Concrete observer that logs calculation events to a log file
- AutoSaverObserver: Concrete observer that automatically saves history when enabled

"""

from abc import ABC, abstractmethod
import logging
from typing import Any
from app.calculation import Calculation


class HistoryObserver(ABC):
    """
    Abstract base class for history observers.
    
    This class defines the interface for observers that monitor and reacts to
    new calculation events in the history management system.

    Implementing classes should provide concrete implementations of the `update` method
    to handle new Calculation events.
    """
    
    
    @abstractmethod
    def update(self, calculation: Calculation) -> None:
        """
        Handle new calculation event.

        Args:
            calculation (Calculation): The calculation that was performed.
        """
        pass # pragma: no cover


class LoggingObserver(HistoryObserver):
    """
    Observer that logs new Calculation events.
    
    Implements the Observer pattern by looking for new Calculation events
    logging their details to a log file.

    """

    def update(self, calculation: Calculation) -> None:
        """
        Log the details of a new Calculation event.
        
        Args:
            calculation (Calculation): The Calculation that was performed.
        """
        if calculation is None:
            raise AttributeError("Calculation cannot be None")
        logging.info(
            f"Calculation performed: {calculation.operation.lower()} "
            f"({calculation.operand1}, {calculation.operand2}) = "
            f"{calculation.result}"
        )
    

class AutoSaverObserver(HistoryObserver):
    """
    Observer that automatically saves Calculation history.
    
    Implements the Observer pattern by looking for new Calculation events
    and saving the history to a file.

    """


    def __init__(self, calculator: Any) -> None:
        """
        Initialize the AutoSaveObserver.
        
        Args:
            calculator (Any): The calculator instance to observe,
            must have 'config' and 'save_history' attributes.

        Raises:
            TypeError: If the calculator does not have the required attributes.
        """
        if not hasattr(calculator, 'config') or not hasattr(calculator, 'save_history'):
            raise TypeError("Calculator must have 'config' and 'save_history' attributes")
        self.calculator = calculator

    def update(self, calculation: Calculation) -> None:
        """
        Trigger auto-save of Calculation history.

        This method is called when a new Calculation event occurs,
        if the calculator's auto-save feature is enabled, it 
        saves the current history to a file.

        Args:
            calculation (Calculation): The Calculation that was performed.
        """
        if calculation is None:
            raise AttributeError("Calculation cannot be None")
        if self.calculator.config.auto_save:
            self.calculator.save_history()
            logging.info("History auto-saved after new calculation.")
    



