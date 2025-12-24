#!/usr/bin/env python3
"""
Main application file for the sample project.
This demonstrates a simple calculator program.
"""

from calculator import Calculator
from utils import format_result


def main():
    """Main function to run the calculator application."""
    calc = Calculator()
    
    print("Simple Calculator Program")
    print("=========================")
    
    # Perform some calculations
    result1 = calc.add(10, 5)
    print(f"10 + 5 = {format_result(result1)}")
    
    result2 = calc.subtract(20, 8)
    print(f"20 - 8 = {format_result(result2)}")
    
    result3 = calc.multiply(6, 7)
    print(f"6 × 7 = {format_result(result3)}")
    
    result4 = calc.divide(100, 4)
    print(f"100 ÷ 4 = {format_result(result4)}")
    
    print("\nCalculation complete!")


if __name__ == "__main__":
    main()