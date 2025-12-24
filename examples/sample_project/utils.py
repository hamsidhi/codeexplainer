"""
Utility functions for formatting and helper operations.
This module provides helper functions used throughout the application.
"""


def format_result(value: float, decimals: int = 2) -> str:
    """
    Format a numeric result with specified decimal places.
    
    Args:
        value: The numeric value to format
        decimals: Number of decimal places (default: 2)
        
    Returns:
        Formatted string representation of the value
    """
    return f"{value:.{decimals}f}"


def validate_number(value) -> bool:
    """
    Check if a value is a valid number.
    
    Args:
        value: Value to validate
        
    Returns:
        True if value is a number, False otherwise
    """
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def get_operation_symbol(operation: str) -> str:
    """
    Get the symbol for a mathematical operation.
    
    Args:
        operation: Operation name ('add', 'subtract', 'multiply', 'divide')
        
    Returns:
        Mathematical symbol for the operation
    """
    symbols = {
        'add': '+',
        'subtract': '-',
        'multiply': '×',
        'divide': '÷'
    }
    return symbols.get(operation, '?')


def create_result_string(operation: str, a: float, b: float, result: float) -> str:
    """
    Create a formatted result string for display.
    
    Args:
        operation: Operation name
        a: First operand
        b: Second operand
        result: Calculation result
        
    Returns:
        Formatted result string
    """
    symbol = get_operation_symbol(operation)
    return f"{format_result(a)} {symbol} {format_result(b)} = {format_result(result)}"