##########################
# main.py
##########################

"""
Main entry point for the calculator application.
This module initializes the calculator REPL (Read-Eval-Print Loop) interface,
allowing users to interactively perform calculations, manage history, and utilize advanced features.

"""

from app.calculator_repl import start_calculator_repl

# Start the calculator REPL when the script is executed
if __name__ == "__main__":
    start_calculator_repl()