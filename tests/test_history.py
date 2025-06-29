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


