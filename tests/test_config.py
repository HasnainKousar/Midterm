###########################
# test_config.py
###########################

"""
Test module for CalculatorConfig class.

This module contains comprehensive unit tests for the CalculatorConfig class,
which manages configuration settings for the calculator application.


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

def clear_env_vars(*args):
    for var in args:
        os.environ.pop(var, None)



def test_default_config():
    config = CalculatorConfig()
    
    assert config.max_history_size == 100
    assert config.auto_save is True
    assert config.precision == 5
    assert config.max_input_value == Decimal('1000000')
    assert config.default_encoding == 'utf-8'
    assert config.log_dir == Path('./test_logs').resolve()
    assert config.history_dir == Path('./test_history').resolve()
    assert config.log_file == Path('./test_logs/test_log.log').resolve()
    assert config.history_file == Path('./test_history/test_history.csv').resolve()

def test_custom_config():
    """Test custom configuration settings."""
    config = CalculatorConfig(
        max_history_size=1000,
        auto_save=True,
        precision=6,
        max_input_value=Decimal('5000'),
        default_encoding='ascii',
    )
    assert config.max_history_size == 1000
    assert config.auto_save is True
    assert config.precision == 6
    assert config.max_input_value == Decimal('5000')
    assert config.default_encoding == 'ascii'


def test_dir_properties():
    """Test directory properties."""
    clear_env_vars('CALCULATOR_LOG_DIR', 'CALCULATOR_HISTORY_DIR')
    config = CalculatorConfig(base_dir=Path('./custom_base_dir'))
    assert config.log_dir == Path('./custom_base_dir/logs').resolve()
    assert config.history_dir == Path('./custom_base_dir/history').resolve()


def test_file_properties():
    """Test file properties."""
    clear_env_vars('CALCULATOR_LOG_FILE', 'CALCULATOR_HISTORY_FILE')
    config = CalculatorConfig(base_dir=Path('./custom_base_dir'))
    assert config.log_file == Path('./custom_base_dir/logs/calculator.log').resolve()
    assert config.history_file == Path('./custom_base_dir/history/calculator_history.csv').resolve()

def test_invalid_max_history_size():
    """Test invalid max history size."""
    with pytest.raises(ConfigurationError, match="Maximum history size must be a positive integer."):
        config = CalculatorConfig(max_history_size=-1)
        config.validate()

def test_invalid_precision():
    """Test invalid precision."""
    with pytest.raises(ConfigurationError, match="Precision must be a non-negative integer."):
        config = CalculatorConfig(precision=-1)
        config.validate()



def test_invalid_max_input_value():
    """Test invalid max input value."""
    with pytest.raises(ConfigurationError, match="Maximum input value must be a positive number."):
        config = CalculatorConfig(max_input_value=Decimal('-10'))
        config.validate()



