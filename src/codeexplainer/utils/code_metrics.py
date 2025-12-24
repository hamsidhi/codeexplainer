from typing import Any
"""
Code metrics calculation utilities

Calculates complexity metrics and other code analysis statistics.
"""

from typing import Dict, Any, Optional
import tree_sitter
from tree_sitter import Node
from loguru import logger


def calculate_complexity_metrics(root_node: Node, language: str) -> dict[str, Any]:
    """
    Calculate code complexity metrics from AST.
    
    Args:
        root_node: Root node of the AST
        language: Programming language
        
    Returns:
        Dictionary containing complexity metrics
    """
    metrics = {
        "score": 0,
        "cyclomatic": 0,
        "cognitive": 0,
        "nesting_depth": 0,
        "max_nesting": 0,
    }
    
    try:
        # Calculate cyclomatic complexity
        metrics["cyclomatic"] = calculate_cyclomatic_complexity(root_node, language)
        
        # Calculate cognitive complexity
        metrics["cognitive"] = calculate_cognitive_complexity(root_node, language)
        
        # Calculate nesting depth
        nesting_result = calculate_nesting_depth(root_node, language)
        metrics["nesting_depth"] = nesting_result["average"]
        metrics["max_nesting"] = nesting_result["maximum"]
        
        # Overall complexity score (weighted combination)
        metrics["score"] = (
            metrics["cyclomatic"] * 0.4 +
            metrics["cognitive"] * 0.4 +
            metrics["max_nesting"] * 0.2
        )
        
    except Exception as e:
        logger.warning(f"Error calculating complexity metrics: {e}")
        metrics["score"] = 1  # Default to simple
    
    return metrics


def calculate_cyclomatic_complexity(root_node: Node, language: str) -> int:
    """
    Calculate cyclomatic complexity from AST.
    
    Cyclomatic complexity = Number of decision points + 1
    
    Args:
        root_node: Root node of the AST
        language: Programming language
        
    Returns:
        Cyclomatic complexity score
    """
    complexity = 1  # Base complexity
    
    # Define decision point node types for different languages
    decision_nodes = {
        "python": [
            "if_statement",
            "elif_clause",
            "while_statement",
            "for_statement",
            "except_clause",
            "with_statement",
            "and",
            "or",
        ],
        "javascript": [
            "if_statement",
            "else_clause",
            "while_statement",
            "for_statement",
            "for_in_statement",
            "do_statement",
            "switch_statement",
            "case",
            "catch_clause",
            "logical_and",
            "logical_or",
            "ternary_expression",
        ],
        "java": [
            "if_statement",
            "else_clause",
            "while_statement",
            "for_statement",
            "enhanced_for_statement",
            "do_statement",
            "switch_statement",
            "case",
            "catch_clause",
            "conditional_expression",
            "logical_and",
            "logical_or",
        ],
        "cpp": [
            "if_statement",
            "else_clause",
            "while_statement",
            "for_statement",
            "range_for_statement",
            "do_statement",
            "switch_statement",
            "case",
            "catch_clause",
            "conditional_expression",
            "logical_and",
            "logical_or",
        ],
    }
    
    # Get decision nodes for the language
    lang_decision_nodes = decision_nodes.get(language, decision_nodes["python"])
    
    def count_decisions(node: Node):
        nonlocal complexity
        
        # Count this node if it's a decision point
        if node.type in lang_decision_nodes:
            complexity += 1
        
        # Recursively count child nodes
        for child in node.children:
            count_decisions(child)
    
    count_decisions(root_node)
    
    return complexity


def calculate_cognitive_complexity(root_node: Node, language: str) -> int:
    """
    Calculate cognitive complexity from AST.
    
    Cognitive complexity measures how hard the code is to understand.
    
    Args:
        root_node: Root node of the AST
        language: Programming language
        
    Returns:
        Cognitive complexity score
    """
    complexity = 0
    
    # Define complexity-increasing constructs
    complexity_increasers = {
        "python": {
            "if_statement": 1,
            "elif_clause": 1,
            "else_clause": 1,
            "while_statement": 1,
            "for_statement": 1,
            "except_clause": 1,
            "with_statement": 1,
            "and": 1,
            "or": 1,
            "lambda": 1,
            "list_comprehension": 1,
            "dictionary_comprehension": 1,
            "generator_expression": 1,
        },
        "javascript": {
            "if_statement": 1,
            "else_clause": 1,
            "while_statement": 1,
            "for_statement": 1,
            "for_in_statement": 1,
            "do_statement": 1,
            "switch_statement": 1,
            "case": 1,
            "catch_clause": 1,
            "logical_and": 1,
            "logical_or": 1,
            "ternary_expression": 1,
            "arrow_function": 1,
        },
        "java": {
            "if_statement": 1,
            "else_clause": 1,
            "while_statement": 1,
            "for_statement": 1,
            "enhanced_for_statement": 1,
            "do_statement": 1,
            "switch_statement": 1,
            "case": 1,
            "catch_clause": 1,
            "conditional_expression": 1,
            "logical_and": 1,
            "logical_or": 1,
            "lambda_expression": 1,
        },
        "cpp": {
            "if_statement": 1,
            "else_clause": 1,
            "while_statement": 1,
            "for_statement": 1,
            "range_for_statement": 1,
            "do_statement": 1,
            "switch_statement": 1,
            "case": 1,
            "catch_clause": 1,
            "conditional_expression": 1,
            "logical_and": 1,
            "logical_or": 1,
            "lambda_expression": 1,
        },
    }
    
    # Get complexity rules for the language
    lang_rules = complexity_increasers.get(language, complexity_increasers["python"])
    
    def calculate_complexity(node: Node, nesting_level: int = 0):
        nonlocal complexity
        
        # Add complexity for this node
        if node.type in lang_rules:
            complexity += lang_rules[node.type]
            
            # Add extra complexity for nesting
            if nesting_level > 0:
                complexity += nesting_level
        
        # Increase nesting level for certain constructs
        new_nesting = nesting_level
        if node.type in ["if_statement", "while_statement", "for_statement", "function_definition", "class_definition"]:
            new_nesting += 1
        
        # Recursively process children
        for child in node.children:
            calculate_complexity(child, new_nesting)
    
    calculate_complexity(root_node)
    
    return complexity


def calculate_nesting_depth(root_node: Node, language: str) -> dict[str, int]:
    """
    Calculate nesting depth metrics from AST.
    
    Args:
        root_node: Root node of the AST
        language: Programming language
        
    Returns:
        Dictionary with average and maximum nesting depth
    """
    nesting_levels = []
    
    # Define constructs that increase nesting
    nesting_constructs = {
        "python": [
            "if_statement",
            "while_statement",
            "for_statement",
            "function_definition",
            "class_definition",
            "with_statement",
            "try_statement",
            "except_clause",
        ],
        "javascript": [
            "if_statement",
            "while_statement",
            "for_statement",
            "for_in_statement",
            "do_statement",
            "function_declaration",
            "arrow_function",
            "function_expression",
            "class_declaration",
            "switch_statement",
            "catch_clause",
        ],
        "java": [
            "if_statement",
            "while_statement",
            "for_statement",
            "enhanced_for_statement",
            "do_statement",
            "method_declaration",
            "class_declaration",
            "switch_statement",
            "catch_clause",
        ],
        "cpp": [
            "if_statement",
            "while_statement",
            "for_statement",
            "range_for_statement",
            "do_statement",
            "function_definition",
            "class_specifier",
            "switch_statement",
            "catch_clause",
        ],
    }
    
    lang_nesting = nesting_constructs.get(language, nesting_constructs["python"])
    
    def find_nesting_levels(node: Node, current_depth: int = 0):
        # Record current depth if this is a significant node
        if node.type in lang_nesting or node.type.endswith("_statement") or node.type.endswith("_definition"):
            nesting_levels.append(current_depth)
        
        # Process children with increased depth for nesting constructs
        for child in node.children:
            new_depth = current_depth
            if node.type in lang_nesting:
                new_depth += 1
            find_nesting_levels(child, new_depth)
    
    find_nesting_levels(root_node)
    
    if not nesting_levels:
        return {"average": 0, "maximum": 0}
    
    return {
        "average": round(sum(nesting_levels) / len(nesting_levels)),
        "maximum": max(nesting_levels),
    }


def calculate_halstead_metrics(source_code: str) -> dict[str, float]:
    """
    Calculate Halstead complexity metrics.
    
    Halstead metrics measure the complexity of the vocabulary used.
    
    Args:
        source_code: Source code text
        
    Returns:
        Dictionary with Halstead metrics
    """
    # This is a simplified implementation
    # Full implementation would require language-specific tokenization
    
    lines = source_code.split('\n')
    
    # Count operators and operands (simplified)
    operators = set(['+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=', '&&', '||', '!'])
    operands = set()
    
    operator_count = 0
    operand_count = 0
    
    for line in lines:
        # Skip comments and strings (simplified)
        if line.strip().startswith('#') or line.strip().startswith('//'):
            continue
        
        words = line.split()
        for word in words:
            # Check if it's an operator
            if word in operators:
                operator_count += 1
                operands.add(word)
            # Check if it's a keyword or identifier
            elif word.isalnum() and not word.isdigit():
                operand_count += 1
                operands.add(word)
    
    # Calculate metrics
    n1 = len([op for op in operands if op in operators])  # Unique operators
    n2 = len([op for op in operands if op not in operators])  # Unique operands
    N1 = operator_count  # Total operators
    N2 = operand_count   # Total operands
    
    if n1 == 0 or n2 == 0:
        return {
            "vocabulary": 0,
            "length": 0,
            "volume": 0,
            "difficulty": 0,
            "effort": 0,
        }
    
    vocabulary = n1 + n2
    length = N1 + N2
    volume = length * (vocabulary.bit_length()) if vocabulary > 0 else 0
    difficulty = (n1 / 2) * (N2 / n2) if n2 > 0 else 0
    effort = difficulty * volume
    
    return {
        "vocabulary": vocabulary,
        "length": length,
        "volume": volume,
        "difficulty": difficulty,
        "effort": effort,
    }


def calculate_maintainability_index(source_code: str, complexity_metrics: dict[str, Any]) -> float:
    """
    Calculate maintainability index.
    
    The maintainability index is a composite metric that indicates
    how easy the code is to maintain.
    
    Args:
        source_code: Source code text
        complexity_metrics: Complexity metrics dictionary
        
    Returns:
        Maintainability index (0-100, higher is better)
    """
    # Calculate lines of code
    lines = source_code.split('\n')
    loc = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
    
    # Get complexity values
    cyclomatic = complexity_metrics.get("cyclomatic", 1)
    halstead_volume = complexity_metrics.get("halstead", {}).get("volume", 1)
    
    # Avoid division by zero
    if loc == 0:
        return 100.0
    
    # Calculate maintainability index
    # Formula: 171 - 5.2 * ln(Halstead Volume) - 0.23 * (Cyclomatic Complexity) - 16.2 * ln(Lines of Code)
    import math
    
    try:
        mi = 171 - 5.2 * math.log(halstead_volume) - 0.23 * cyclomatic - 16.2 * math.log(loc)
        
        # Normalize to 0-100 scale
        mi = max(0, min(100, mi))
        
        return mi
        
    except (ValueError, ZeroDivisionError):
        return 50.0  # Default moderate maintainability