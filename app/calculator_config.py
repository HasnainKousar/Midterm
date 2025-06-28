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

