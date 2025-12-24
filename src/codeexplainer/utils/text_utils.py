from typing import Any
"""
Text processing utilities for CodeExplainer

Handles text simplification, technical term translation,
and audio optimization for explanations.
"""

import re
from typing import List, Dict, Any
from num2words import num2words


def simplify_technical_terms(text: str, language: str = "python") -> str:
    """
    Replace technical terms with beginner-friendly alternatives.
    
    Args:
        text: Original technical text
        language: Programming language context
        
    Returns:
        Simplified text
    """
    # Common technical term simplifications
    simplifications = {
        # Programming concepts
        "function": "tool or recipe",
        "method": "action or behavior",
        "class": "blueprint or template",
        "object": "thing or item",
        "variable": "container or box",
        "parameter": "input or ingredient",
        "argument": "specific input",
        "return": "give back or output",
        "import": "bring in or borrow",
        "export": "share or send out",
        "module": "toolbox or collection",
        "package": "group of tools",
        "library": "collection of useful tools",
        "framework": "foundation or structure",
        "algorithm": "step-by-step plan",
        "loop": "repeat something",
        "condition": "check or test",
        "boolean": "true or false",
        "string": "text or words",
        "integer": "whole number",
        "float": "decimal number",
        "array": "list of items",
        "list": "collection of items",
        "dictionary": "lookup table",
        "hash": "unique fingerprint",
        "exception": "error or problem",
        "debug": "find and fix problems",
        "compile": "translate to computer language",
        "execute": "run or do",
        "instantiate": "create or make",
        "inherit": "get features from parent",
        "override": "replace or change",
        "implement": "make it work",
        "initialize": "set up or prepare",
        "terminate": "stop or end",
        "iterate": "go through one by one",
        "recursion": "function calling itself",
        
        # File and system terms
        "directory": "folder",
        "repository": "project folder",
        "commit": "save changes",
        "push": "send to server",
        "pull": "get from server",
        "merge": "combine changes",
        "branch": "separate version",
        "conflict": "disagreement between changes",
        
        # Web terms
        "API": "way for programs to talk to each other",
        "endpoint": "specific address for requests",
        "request": "ask for something",
        "response": "answer back",
        "JSON": "data format",
        "REST": "way to organize web services",
        "HTTP": "language websites use to communicate",
        "URL": "web address",
        "server": "computer that provides information",
        "client": "computer that asks for information",
        
        # Database terms
        "database": "organized collection of information",
        "query": "ask for specific information",
        "table": "organized list of data",
        "column": "category of information",
        "row": "one piece of information",
        "index": "fast way to find information",
        "primary key": "unique identifier",
        "foreign key": "link to information in another table",
        
        # Development terms
        "IDE": "program for writing code",
        "version control": "track changes to code",
        "refactor": "reorganize code to make it better",
        "deploy": "put code where others can use it",
        "production": "live version that users see",
        "staging": "test version before going live",
        "development": "version while building and testing",
        "environment": "setup where code runs",
        "dependency": "other code this needs to work",
        "build": "prepare code to run",
        "test": "check if code works correctly",
        "lint": "check code style and quality",
        "format": "make code look consistent",
    }
    
    # Language-specific simplifications
    language_simplifications = {
        "python": {
            "def": "define a function",
            "self": "the current object",
            "__init__": "setup function",
            "if __name__ == '__main__'": "run this only when file is executed directly",
            "lambda": "small, quick function",
            "comprehension": "compact way to create lists",
            "decorator": "function that modifies another function",
            "generator": "function that gives results one at a time",
        },
        "javascript": {
            "const": "value that doesn't change",
            "let": "value that can change",
            "var": "old way to declare variables",
            "function": "define a function",
            "=>": "arrow function (short way to write functions)",
            "async": "do something while waiting",
            "await": "wait for something to finish",
            "Promise": "something that will happen in the future",
            "callback": "function to run later",
        },
        "java": {
            "public": "everyone can use this",
            "private": "only this class can use this",
            "protected": "this class and children can use this",
            "static": "belongs to the class, not objects",
            "final": "cannot be changed",
            "abstract": "outline that needs to be filled in",
            "interface": "contract that classes must follow",
            "synchronized": "only one at a time",
        },
    }
    
    # Apply general simplifications
    result = text
    for technical, simple in simplifications.items():
        pattern = r'\b' + re.escape(technical) + r'\b'
        result = re.sub(pattern, simple, result, flags=re.IGNORECASE)
    
    # Apply language-specific simplifications
    if language in language_simplifications:
        for technical, simple in language_simplifications[language].items():
            pattern = re.escape(technical)
            result = re.sub(pattern, simple, result)
    
    return result


def optimize_for_tts(text: str) -> str:
    """
    Optimize text for text-to-speech narration.
    
    Args:
        text: Original text
        
    Returns:
        Text optimized for TTS
    """
    # Convert numbers to words for better pronunciation
    def convert_numbers(match):
        number = int(match.group())
        return num2words(number)
    
    # Convert standalone numbers
    text = re.sub(r'\b\d+\b', convert_numbers, text)
    
    # Convert common abbreviations
    abbreviations = {
        "e.g.": "for example",
        "i.e.": "that is",
        "etc.": "and so on",
        "vs.": "versus",
        "Dr.": "Doctor",
        "Mr.": "Mister",
        "Mrs.": "Missus",
        "Ms.": "Miss",
        "Jr.": "Junior",
        "Sr.": "Senior",
        "Inc.": "Incorporated",
        "Ltd.": "Limited",
        "Co.": "Company",
        "Corp.": "Corporation",
        "Ave.": "Avenue",
        "St.": "Street",
        "Blvd.": "Boulevard",
        "Rd.": "Road",
        "Apt.": "Apartment",
        "Dept.": "Department",
        "Gov.": "Government",
        "Sen.": "Senator",
        "Rep.": "Representative",
        "Pres.": "President",
        "CEO": "Chief Executive Officer",
        "CFO": "Chief Financial Officer",
        "CTO": "Chief Technology Officer",
        "HTML": "H T M L",
        "CSS": "C S S",
        "API": "A P I",
        "URL": "U R L",
        "HTTP": "H T T P",
        "HTTPS": "H T T P S",
        "FTP": "F T P",
        "SQL": "S Q L",
        "JSON": "J S O N",
        "XML": "X M L",
        "YAML": "Y A M L",
        "PDF": "P D F",
        "JPG": "J P G",
        "PNG": "P N G",
        "GIF": "G I F",
        "SVG": "S V G",
        "CPU": "C P U",
        "GPU": "G P U",
        "RAM": "R A M",
        "ROM": "R O M",
        "SSD": "S S D",
        "HDD": "H D D",
        "USB": "U S B",
        "HDMI": "H D M I",
        "WiFi": "Wi Fi",
        "AI": "A I",
        "ML": "M L",
        "UI": "U I",
        "UX": "U X",
        "GUI": "G U I",
        "CLI": "C L I",
        "OS": "O S",
        "PC": "P C",
        "Mac": "Mac",
        "iOS": "i O S",
        "Android": "Android",
    }
    
    for abbrev, full in abbreviations.items():
        text = re.sub(r'\b' + re.escape(abbrev) + r'\b', full, text, flags=re.IGNORECASE)
    
    # Add pauses after periods for better flow
    text = re.sub(r'\.', '. ', text)
    text = re.sub(r'\s+', ' ', text)  # Clean up extra spaces
    
    # Break up long sentences
    sentences = text.split('. ')
    if len(sentences) > 5:
        # Add paragraph breaks for long texts
        mid_point = len(sentences) // 2
        text = '. '.join(sentences[:mid_point]) + '.\n\n' + '. '.join(sentences[mid_point:])
    
    return text.strip()


def extract_key_concepts(text: str, language: str = "python") -> list[str]:
    """
    Extract key programming concepts from text.
    
    Args:
        text: Source text
        language: Programming language context
        
    Returns:
        List of key concepts found
    """
    # Common programming concepts to highlight
    concepts = {
        "python": [
            "function", "class", "method", "variable", "import", "if", "for", "while",
            "try", "except", "def", "return", "lambda", "comprehension", "decorator",
            "generator", "module", "package", "inheritance", "polymorphism", "encapsulation",
        ],
        "javascript": [
            "function", "class", "method", "variable", "import", "export", "if", "for", "while",
            "try", "catch", "async", "await", "Promise", "callback", "arrow function",
            "const", "let", "var", "object", "array", "prototype", "closure",
        ],
        "java": [
            "class", "method", "variable", "import", "if", "for", "while", "try", "catch",
            "public", "private", "protected", "static", "final", "abstract", "interface",
            "inheritance", "polymorphism", "encapsulation", "override", "overload",
        ],
    }
    
    found_concepts = []
    language_concepts = concepts.get(language, concepts["python"])
    
    for concept in language_concepts:
        if concept.lower() in text.lower():
            found_concepts.append(concept)
    
    return list(set(found_concepts))


def create_summary(text: str, max_length: int = 100) -> str:
    """
    Create a brief summary of text content.
    
    Args:
        text: Original text
        max_length: Maximum length of summary
        
    Returns:
        Brief summary
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Take first sentence or up to max_length
    sentences = text.split('. ')
    
    if sentences:
        first_sentence = sentences[0]
        if len(first_sentence) <= max_length:
            return first_sentence + '.'
        else:
            # Truncate at word boundary
            truncated = first_sentence[:max_length]
            last_space = truncated.rfind(' ')
            if last_space > 0:
                return truncated[:last_space] + '...'
            else:
                return truncated + '...'
    
    return text[:max_length] + '...' if len(text) > max_length else text


def highlight_code_terms(text: str) -> str:
    """
    Highlight programming terms in text with markdown formatting.
    
    Args:
        text: Original text
        
    Returns:
        Text with highlighted programming terms
    """
    # Common programming terms to highlight
    code_terms = [
        "function", "class", "method", "variable", "import", "export", "return",
        "if", "else", "for", "while", "try", "catch", "def", "const", "let", "var",
        "public", "private", "protected", "static", "new", "this", "self", "super",
    ]
    
    highlighted = text
    for term in code_terms:
        # Use markdown inline code formatting
        pattern = r'\b' + re.escape(term) + r'\b'
        highlighted = re.sub(pattern, f'`{term}`', highlighted, flags=re.IGNORECASE)
    
    return highlighted