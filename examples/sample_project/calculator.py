"""
Calculator module containing mathematical operations.
This module provides basic arithmetic functions for calculations.
"""


class Calculator:
    """A simple calculator class for basic arithmetic operations."""
    
    def __init__(self):
        """Initialize the calculator."""
        self.operations_performed = 0
    
    def add(self, a: float, b: float) -> float:
        """
        Add two numbers together.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Sum of a and b
        """
        self.operations_performed += 1
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """
        Subtract b from a.
        
        Args:
            a: First number
            b: Second number to subtract
            
        Returns:
            Difference of a minus b
        """
        self.operations_performed += 1
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """
        Multiply two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Product of a times b
        """
        self.operations_performed += 1
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """
        Divide a by b.
        
        Args:
            a: Dividend
            b: Divisor
            
        Returns:
            Quotient of a divided by b
            
        Raises:
            ValueError: If b is zero
        """
        if b == 0:
            raise ValueError("Cannot divide by zero")
        
        self.operations_performed += 1
        return a / b
    
    def get_operations_count(self) -> int:
        """
        Get the number of operations performed.
        
        Returns:
            Total number of operations performed
        """
        return self.operations_performed
    
    def reset(self) -> None:
        """Reset the operations counter."""
        self.operations_performed = 0