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
                command = input(f"{Fore.GREEN}Enter command: {Style.RESET_ALL}").lower().strip()

                if command == "help":
                    # Display the available commands
                    print(f"{Fore.GREEN}\nAvailable commands:")
                    print("  add, subtract, multiply, divide, power, root, modulus, integerdivision, percentage, absolutedifference")
                    print("  history - Show calculation history")
                    print("  undo - Undo the last operation")
                    print("  redo - Redo the last undone operation")
                    print("  clear - Clear the history")
                    print("  save - Save the current history to a file")
                    print("  load - Load history from a file")
                    print(f"  exit - Exit the calculator REPL{Style.RESET_ALL}")
                    continue

                if command == "exit":
                    # Attempt to save history before exiting
                    try:
                        calc.save_history()
                        print(f"{Fore.GREEN}History saved successfully.{Style.RESET_ALL}")
                    except OperationError as e:
                        print(f"{Fore.RED}Warning: Could not save history before exiting: {e}{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}Exiting calculator REPL. Goodbye!{Style.RESET_ALL}")
                    break
                if command == "history":
                    # Show the calculation history
                    history = calc.show_history()
                    if not history:
                        print(f"{Fore.GREEN}No calculations performed yet.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.GREEN}\nCalculation History:{Style.RESET_ALL}")
                        for idx, entry in enumerate(history, start=1):
                            print(f"{Fore.GREEN}{idx}. {entry}{Style.RESET_ALL}")
                    continue

                if command == "clear":
                    # Clear the calculation history
                    calc.clear_history()
                    print(f"{Fore.GREEN}History cleared.{Style.RESET_ALL}")
                    continue

                if command == "undo":
                    # Undo the last operation
                    if calc.undo():
                        print(f"{Fore.GREEN}Last operation undone.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.GREEN}No operations to undo.{Style.RESET_ALL}")
                    continue

                if command == "redo":
                    # Redo the last undone operation
                    if calc.redo():
                        print(f"{Fore.GREEN}Last operation redone.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.GREEN}No operations to redo.{Style.RESET_ALL}")
                    continue

                if command == "load":
                    # Load history from a file
                    try:
                        calc.load_history()
                        print(f"{Fore.GREEN}History loaded successfully.{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}Error loading history: {e}{Style.RESET_ALL}")
                    continue

                if command == "save":
                    # Save the current history to a file
                    try:
                        calc.save_history()
                        print(f"{Fore.GREEN}History saved successfully.{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}Error saving history: {e}{Style.RESET_ALL}")
                    continue

                if command in['add', 'subtract', 'multiply', 'divide', 'power', 'root', 'modulus', 'integerdivision', 'percentage', 'absolutedifference']:
                    # Perform a calculation based on the command
                    try:
                        print(f"{Fore.GREEN}\n Enter number (or cancel to abort):{Style.RESET_ALL}")
                        a = input(f"{Fore.GREEN}First number: {Style.RESET_ALL}")
                        if a.lower() == 'cancel':
                            print(f"{Fore.GREEN}Operation cancelled.{Style.RESET_ALL}")
                            continue
                        b = input(f"{Fore.GREEN}Second number: {Style.RESET_ALL}")
                        if b.lower() == 'cancel':
                            print(f"{Fore.GREEN}Operation cancelled.{Style.RESET_ALL}")
                            continue

                        # Create appropriate operation instance using the factory pattern
                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)

                        # Perform the calculation
                        result = calc.perform_operation(a, b)

                        # Normalize the result to Decimal for consistent output
                        if isinstance(result, Decimal):
                            result = result.normalize()
                        
                        print(f"{Fore.GREEN}\nResult: {result}{Style.RESET_ALL}")

                    except (OperationError, ValidationError) as e:
                        # Handle specific operation errors
                        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
                    except Exception as e:
                        # Handle any other unexpected errors
                        print(f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}")
                    continue
                # Handle unknown commands
                print(f"{Fore.GREEN}Unknown command: '{command}'. Type 'help' for available commands.{Style.RESET_ALL}")

            except KeyboardInterrupt:
                # Handle Ctrl+C gracefully
                print(f"{Fore.GREEN}\nOperation cancelled by user.{Style.RESET_ALL}")
                continue
            except EOFError:
                # Handle EOF (Ctrl+D) gracefully
                print(f"{Fore.GREEN}\nInput terminated by user. Exiting REPL....{Style.RESET_ALL}")
                break
            except Exception as e:
                # Catch any other unexpected errors
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
                continue
    except Exception as e:
        # Handle any initialization errors
        print(f"{Fore.RED}Failed to start calculator REPL: {e}{Style.RESET_ALL}")
        logging.error(f"Failed to start calculator REPL: {e}")
        raise 


#Uncomment the following lines to run the REPL when this script is executed directly
# if __name__ == "__main__":
#     # Start the calculator REPL when the script is run directly
#     start_calculator_repl()






            


