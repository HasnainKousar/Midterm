###########################
# test_config.py
###########################

"""

"""


import pytest
import os
from decimal import Decimal
from pathlib import Path
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


# Set up temporary environment variables for testing
os.environ['CALCULATOR_MAX_HISTORY_SIZE'] = '100'
os.environ['CALCULATOR_AUTO_SAVE'] = 'True'
os.environ['CALCULATOR_PRECISION'] = '5'
os.environ['CALCULATOR_MAX_INPUT_VALUE'] = '1000000'
os.environ['CALCULATOR_DEFAULT_ENCODING'] = 'utf-8'
os.environ['CALCULATOR_LOG_DIR'] = './test_logs'
os.environ['CALCULATOR_HISTORY_DIR'] = './test_history'
os.environ['CALCULATOR_LOG_FILE'] = './test_logs/test_log.log'
os.environ['CALCULATOR_HISTORY_FILE'] = './test_history/test_history.csv'

