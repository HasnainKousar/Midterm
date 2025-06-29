#######################
# Advanced Calculator REPL
#######################

"""
THis module provides an advanced REPL (Read-Eval-Print Loop) for the calculator application.
It allows users to interactively perform calculations, manage history, and utilize advanced features like undo/
redo functionality.

"""

from decimal import Decimal
import logging

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory


def start_calculator_repl():
    """
    

    """

    try:
        # Initialize the calculator instance
        calc = Calculator()

        # Register observers for logging and auto-saving history
        calc.add_observer(LoggingObserver())
        calc.add_observer(AutoSaveObserver(calc))

        print("Calculator REPL started. Type 'help' for available commands.")

        while True:
            try:
                # prompt user for a command
                command = input("\nEnter command: ").lower().strip()


                if command == "help":
                    # Display the available commands
                    print("\nAvailable commands:")
                    print("  add, subtract, multiply, divide, power, root, modulus, integerdivide, percentage, absolutedifference")
                    print("  history - Show calculation history")
                    print("  undo - Undo the last operation")
                    print("  redo - Redo the last undone operation")
                    print("  clear - Clear the history")
                    print("  save - Save the current history to a file")
                    print("  load - Load history from a file")
                    print("  exit - Exit the calculator REPL")
                    continue

                if command == "exit":
                    # Attempt to save history before exiting
                    try:
                        calc.save_history()
                        print("History saved successfully.")
                    except OperationError as e:
                        print(f"Warning: Could not save history before exiting: {e}")
                    print("Exiting calculator REPL. Goodbye!")
                    break
                if command == "history":
                    # Show the calculation history
                    history = calc.show_history()
                    if not history:
                        print("No calculations performed yet.")
                    else:
                        print("\nCalculation History:")
                        for idx, entry in enumerate(history, start=1):
                            print(f"{idx}. {entry}")
                    continue

                

