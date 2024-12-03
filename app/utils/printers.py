"""
This module defines utility functions to print messages in the terminal.
These functions will conform themselves to the color codes indicated by FastAPI.
"""

from app.utils.enums.colors import Colors


def print_info(string: str) -> None:
    """
    This function prints an information message in the terminal.
    Uses the green coloration.
    """
    print(f'{Colors.Fg.green}INFO{Colors.reset}:     {string}')

def print_warning(string: str) -> None:
    """
    This function prints a warning message in the terminal.
    Uses the yellow coloration.
    """
    print(f'{Colors.Fg.yellow}WARNING{Colors.reset}:  {string}')

def print_error(string: str) -> None:
    """
    This function prints an error message in the terminal.
    Uses the red coloration.
    """
    print(f'{Colors.Fg.red}ERROR{Colors.reset}:    {string}')
