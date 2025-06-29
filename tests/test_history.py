#########################
# test_history.py
#########################

"""
Unit tests for the history module.

This module contains tests for the observer pattern implementation,
including LoggingObserver and AutoSaverObserver functionality.
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

########################
# Test AutoSaverObserver
########################

def test_autosave_observer_triggers_save():
    calculator_mock = Mock(spec=Calculator)
    calculator_mock.config = CalculatorConfig()
    calculator_mock.config.auto_save = True
    observer = AutoSaverObserver(calculator_mock)
    observer.update(calculation_mock)
    calculator_mock.save_history.assert_called_once()


@patch('logging.info')
def test_autosave_observer_does_not_trigger_save_when_auto_save_disabled(mock_logging_info):
    """Test that AutoSaverObserver does not trigger save when auto_save is False."""
    calculator_mock = Mock(spec=Calculator)
    calculator_mock.config = CalculatorConfig()
    calculator_mock.config.auto_save = False
    observer = AutoSaverObserver(calculator_mock)
    observer.update(calculation_mock)
    calculator_mock.save_history.assert_not_called()
    logging.info.assert_not_called()



######################
# negative test cases
######################

def test_autosave_observer_invalid_calculator():
    """Test AutoSaverObserver raises TypeError if calculator does not have required attributes."""
    with pytest.raises(TypeError):
        AutoSaverObserver(calculator=None)


def test_autosave_observer_no_calculation():
    """Test that AutoSaverObserver does not save if no calculation is provided."""
    calculator_mock = Mock(spec=Calculator)
    calculator_mock.config = Mock(spec=CalculatorConfig)
    calculator_mock.config.auto_save = True
    observer = AutoSaverObserver(calculator_mock)

    with pytest.raises(AttributeError):
        observer.update(None)