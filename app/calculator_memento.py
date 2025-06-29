############################
# calculator_memento.py
############################

"""

"""

from dataclasses import dataclass, field
import datetime
from typing import Any, Dict, List

from app.calculation import Calculation


@dataclass
class CalculatorMemento:
    """
    
    """

    history: List[Calculation] # List of Calculation objects representing the history of calculations.
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)  # Timestamp of when the memento was created.
    

    def to_dict(self) -> Dict[str, Any]:
        """
        
        
        """
        return {
            'history': [calc.to_dict() for calc in self.history],
            'timestamp': self.timestamp.isoformat()
        }
    
