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

