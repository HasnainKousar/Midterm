#######################
# Advanced Calculator REPL
#######################

"""
THis module provides an advanced REPL (Read-Eval-Print Loop) for the calculator application.
It allows users to interactively perform calculations, manage history, and utilize advanced features like undo/
redo functionality.

"""

from calendar import c
from decimal import Decimal
import logging

from colorama import Fore, Style, init as colorama_init
from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaverObserver, LoggingObserver
from app.operations import OperationFactory

colorama_init(autoreset=True)  # Initialize colorama for colored output


def start_calculator_repl():
    """
    Start the calculator REPL (Read-Eval-Print Loop).

    This function initializes the calculator, registers observers for logging and auto-saving history,
    and provides an interactive command-line interface for performing calculations.

    """

    try:
        # Initialize the calculator instance
        calc = Calculator()

        # Register observers for logging and auto-saving history
        calc.add_observer(LoggingObserver())
        calc.add_observer(AutoSaverObserver(calc))

        print(f"{Fore.GREEN}Calculator REPL started. Type 'help' for available commands.{Style.RESET_ALL}")

        while True:
            try:
                # prompt user for a command
                command = input("\nEnter command: ").lower().strip()


                if command == "help":
                    # Display the available commands
                    print("\nAvailable commands:")
                    print("  add, subtract, multiply, divide, power, root, modulus, integerdivision, percentage, absolutedifference")
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

                if command == "clear":
                    # Clear the calculation history
                    calc.clear_history()
                    print("History cleared.")
                    continue

                if command == "undo":
                    # Undo the last operation
                    if calc.undo():
                        print("Last operation undone.")
                    else:
                        print("No operations to undo.")
                    continue

                if command == "redo":
                    # Redo the last undone operation
                    if calc.redo():
                        print("Last operation redone.")
                    else:
                        print("No operations to redo.")
                    continue

                if command == "load":
                    # Load history from a file
                    try:
                        calc.load_history()
                        print("History loaded successfully.")
                    except Exception as e:
                        print(f"Error loading history: {e}")
                    continue

                if command == "save":
                    # Save the current history to a file
                    try:
                        calc.save_history()
                        print("History saved successfully.")
                    except Exception as e:
                        print(f"Error saving history: {e}")
                    continue

                if command in['add', 'subtract', 'multiply', 'divide', 'power', 'root', 'modulus', 'integerdivision', 'percentage', 'absolutedifference']:
                    # Perform a calculation based on the command
                    try:
                        print("\n Enter number (or cancel to abort):")
                        a = input("First number: ")
                        if a.lower() == 'cancel':
                            print("Operation cancelled.")
                            continue
                        b = input("Second number: ")
                        if b.lower() == 'cancel':
                            print("Operation cancelled.")
                            continue

                        # Create appropriate operation instance using the factory pattern
                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)

                        # Perform the calculation
                        result = calc.perform_operation(a, b)

                        # Normalize the result to Decimal for consistent output
                        if isinstance(result, Decimal):
                            result = result.normalize()
                        
                        print(f"\nResult: {result}")

                    except (OperationError, ValidationError) as e:
                        # Handle specific operation errors
                        print(f"Error: {e}")
                    except Exception as e:
                        # Handle any other unexpected errors
                        print(f"An unexpected error occurred: {e}")
                    continue
                # Handle unknown commands
                print(f"Unknown command: '{command}'. Type 'help' for available commands.")

            except KeyboardInterrupt:
                # Handle Ctrl+C gracefully
                print("\nOperation cancelled by user.")
                continue
            except EOFError:
                # Handle EOF (Ctrl+D) gracefully
                print("\nInput terminated by user. Exiting REPL....")
                break
            except Exception as e:
                # Catch any other unexpected errors
                print(f"Error: {e}")
                continue
    except Exception as e:
        # Handle any initialization errors
        print(f"Failed to start calculator REPL: {e}")
        logging.error(f"Failed to start calculator REPL: {e}")
        raise 


#Uncomment the following lines to run the REPL when this script is executed directly
# if __name__ == "__main__":
#     # Start the calculator REPL when the script is run directly
#     start_calculator_repl()






            


