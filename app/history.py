###########################
# History management for the application
###########################

"""

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
    





