########################
# Calculator Config    #
########################

from dataclasses import dataclass
from decimal import Decimal
from numbers import Number
from pathlib import Path
import os
from typing import Optional

from dotenv import load_dotenv

from app.exceptions import ConfigurationError

# Load environment variables from a .env file into the program's environment
load_dotenv()


def get_project_root() -> Path:
    """
    Get the root directory of the project.
    """
    current_file = Path(__file__)

    return current_file.parent.parent


@dataclass
class CalculatorConfig:
    """
    Configuration for the calculator application.
    
    This class holds configuration settings for the calculator, including
    the precision for decimal operations, directory paths, history size, 
    auto-save preference, maximum input values, and default encoding.
    
    Configurations are loaded from environment variables or by passing
    parameters directly to the class constructor.
    
    """
    def __init__(
             self,
        base_dir: Optional[Path] = None,
        max_history_size: Optional[int] = None,
        auto_save: Optional[bool] = None,
        precision: Optional[int] = None,
        max_input_value: Optional[Number] = None,
        default_encoding: Optional[str] = None,
    ):
        
        """
        Initialize the CalculatorConfig with default or provided values.
        
        Args:
            base_dir (Path, optional): Base directory for the application.
            max_history_size (int, optional): Maximum size of the calculation history.
            auto_save (bool, optional): Whether to auto-save the calculation history.
            precision (int, optional): Decimal precision for calculations.
            max_input_value (Number, optional): Maximum value for input operands.
            default_encoding (str, optional): Default encoding for string operations.
        """

        # set base directory to project root by default
        project_root = get_project_root()
        self.base_dir = base_dir or Path(
            os.getenv('CALCULATOR_BASE_DIR', str(project_root))
        ).resolve()


        # set max history size to 1000 by default
        self.max_history_size = max_history_size or int(
            os.getenv('CALCULATOR_MAX_HISTORY_SIZE', 1000)
        )

        # set auto save to True by default
        self.auto_save = auto_save if auto_save is not None else bool(
            os.getenv('CALCULATOR_AUTO_SAVE', True)
        )

        # set precision to 10 by default
        self.precision = precision or int(
            os.getenv('CALCULATOR_PRECISION', 10)
        )

        # set max input value to 1000000 by default
        self.max_input_value = max_input_value or Decimal(
            os.getenv('CALCULATOR_MAX_INPUT_VALUE', 1000000)
        )
    
        # set default encoding to utf-8 by default
        self.default_encoding = default_encoding or os.getenv(
            'CALCULATOR_DEFAULT_ENCODING', 'utf-8'
        )

    @property
    def log_dir(self) -> Path:
        """
        Get the log directory path.
            
        Determines the directory path where log files will be stored.

        Returns:
            Path: The path to the log directory. 
        """
        return Path(
            os.getenv('CALCULATOR_LOG_DIR', str(self.base_dir / 'logs'))
        ).resolve()
    

    @property
    def history_dir(self) -> Path:
        """
        Get the history directory path.
        
        Determines the directory path where calculation history files will be stored.

        Returns:
            Path: The path to the history directory.
        """
        return Path(
            os.getenv('CALCULATOR_HISTORY_DIR', str(self.base_dir / 'history'))
        ).resolve()
    
    @property
    def log_file(self) -> Path:
        """
        Get the log file path.
        
        Determines the file path for the log file.

        Returns:
            Path: The path to the log file.
        """
        return Path(
            os.getenv('CALCULATOR_LOG_FILE', str(self.log_dir / 'calculator.log'))
        ).resolve()
    
    @property
    def history_file(self) -> Path:
        """
        Get the history file path.
        
        Determines the file path for the calculation history file.

        Returns:
            Path: The path to the history file.
        """
        return Path(
            os.getenv('CALCULATOR_HISTORY_FILE', str(self.history_dir / 'calculator_history.csv'))
        ).resolve()
    
    def validate(self):
        """
        Validate the configuration settings.
        
        Checks if the configuration values are within acceptable ranges and formats.
        
        Raises:
            ConfigurationError: If any configuration value is invalid.
        """
        if self.max_history_size <= 0:
            raise ConfigurationError("Maximum history size must be a positive integer.")
        
        if self.precision < 0:
            raise ConfigurationError("Precision must be a non-negative integer.")
        
        if self.max_input_value <= 0:
            raise ConfigurationError("Maximum input value must be a positive number.")
        
    