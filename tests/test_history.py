#########################
# test_history.py
#########################

"""

"""

import logging
import pytest
from unittest.mock import Mock, patch
from app.calculation import Calculation
from app.history import LoggingObserver, AutoSaverObserver
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig


# sample set up for mock calculation
calculation_mock = Mock(spec=Calculation)
calculation_mock.operation = 'Addition'
calculation_mock.operand1 = 6
calculation_mock.operand2 = 2
calculation_mock.result = 8


#######################
# Test LoggingObserver
#######################

@patch('logging.info')
def test_logging_observer_logs_calculation(mock_logging_info):
    """Test that LoggingObserver logs the calculation correctly."""
    observer = LoggingObserver()
    observer.update(calculation_mock)
    logging.info.assert_called_once_with(
        f"Calculation performed: addition (6, 2) = 8"
    )

def test_logging_observer_none_calculation():
    """Test LoggingObserver raises AttributeError when calculation is None."""
    observer = LoggingObserver()
    with pytest.raises(AttributeError):
        observer.update(None)

