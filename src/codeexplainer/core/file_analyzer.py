from typing import Any
"""
FileAnalyzer - Analyzes individual source code files

This module uses tree-sitter and other parsing libraries to deeply
analyze the structure and purpose of source code files.
"""

import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import tree_sitter
from tree_sitter import Language, Parser, Node
from loguru import logger

from ..parsers import get_parser_for_language, get_language_mapping
from ..utils.code_metrics import calculate_complexity_metrics


class FileAnalyzer:
    """Analyzes individual source code files to understand their structure and purpose."""
    
    def __init__(self, analysis_config: dict[str, Any]):
        """
        Initialize the file analyzer.
        
        Args:
            analysis_config: Configuration for analysis behavior
        """
        self.config = analysis_config
        self.language_mapping = get_language_mapping()
        
        # Initialize tree-sitter parsers
        self.parsers = {}
        
        logger.info("FileAnalyzer initialized")
    
    def analyze(self, file_path: Path, language: Optional[str] = None) -> Optional[dict[str, Any]]:
        """
        Analyze a single source code file.
        
        Args:
            file_path: Path to the file to analyze
            language: Override language detection
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Read file content
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                source_code = f.read()
            
            if not source_code.strip():
                logger.warning(f"Empty file: {file_path}")
                return None
            
            # Detect language if not provided
            if not language:
                language = self._detect_language(file_path, source_code)
            
            if not language:
                logger.warning(f"Could not detect language for: {file_path}")
                return None
            
            # Get tree-sitter parser
            parser = self._get_parser(language)
            
            if not parser:
                logger.warning(f"No parser available for language: {language}")
                return self._analyze_without_parser(file_path, source_code, language)
            
            # Parse the code
            tree = parser.parse(bytes(source_code, "utf-8"))
            
            # Analyze the AST
            analysis = self._analyze_ast(
                tree=tree,
                source_code=source_code,
                file_path=file_path,
                language=language
            )
            
            return analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze {file_path}: {e}")
            return None
    
    def _detect_language(self, file_path: Path, source_code: str) -> Optional[str]:
        """
        Detect programming language from file content.
        
        Args:
            file_path: Path to the file
            source_code: Content of the file
            
        Returns:
            Language name or None
        """
        # Use extension as primary method
        extension = file_path.suffix.lower()
        
        # Map common extensions to languages
        extension_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".jsx": "javascript",
            ".tsx": "typescript",
            ".java": "java",
            ".cpp": "cpp",
            ".cxx": "cpp",
            ".cc": "cpp",
            ".c": "c",
            ".h": "c",
            ".hpp": "cpp",
            ".go": "go",
            ".rs": "rust",
            ".rb": "ruby",
            ".php": "php",
            ".swift": "swift",
            ".kt": "kotlin",
            ".sh": "bash",
            ".ps1": "powershell",
            ".pl": "perl",
            ".lua": "lua",
        }
        
        if extension in extension_map:
            return extension_map[extension]
        
        # Try to detect from shebang or content patterns
        first_line = source_code.split("\n")[0].strip() if source_code else ""
        
        shebang_map = {
            "#!/usr/bin/env python": "python",
            "#!/usr/bin/python": "python",
            "#!/bin/bash": "bash",
            "#!/usr/bin/env bash": "bash",
            "#!/bin/sh": "bash",
            "#!/usr/bin/perl": "perl",
            "#!/usr/bin/env node": "javascript",
        }
        
        for shebang, lang in shebang_map.items():
            if first_line.startswith(shebang):
                return lang
        
        return None
    
    def _get_parser(self, language: str) -> Optional[Parser]:
        """
        Get or create a tree-sitter parser for the given language.
        
        Args:
            language: Language name
            
        Returns:
            Tree-sitter parser or None if not available
        """
        if language in self.parsers:
            return self.parsers[language]
        
        # Get parser from the parsers module
        parser = get_parser_for_language(language)
        
        if parser:
            self.parsers[language] = parser
        
        return parser
    
    def _analyze_ast(
        self,
        tree: tree_sitter.Tree,
        source_code: str,
        file_path: Path,
        language: str
    ) -> dict[str, Any]:
        """
        Analyze the Abstract Syntax Tree of the source code.
        
        Args:
            tree: Parsed AST tree
            source_code: Original source code
            file_path: Path to the file
            language: Detected language
            
        Returns:
            Dictionary containing analysis results
        """
        root_node = tree.root_node
        
        # Extract different types of information
        analysis = {
            "file_path": str(file_path),
            "filename": file_path.name,
            "language": language,
            "size": len(source_code),
            "metrics": self._extract_metrics(source_code, root_node, language),
            "purpose": self._determine_purpose(source_code, root_node, language),
            "structure": self._analyze_structure(root_node, source_code, language),
            "dependencies": self._extract_dependencies(root_node, source_code, language),
            "functions": self._extract_functions(root_node, source_code, language),
            "classes": self._extract_classes(root_node, source_code, language),
        }
        
        return analysis
    
    def _extract_metrics(self, source_code: str, root_node: Node, language: str) -> dict[str, Any]:
        """Extract code metrics like lines, complexity, etc."""
        lines = source_code.split("\n")
        
        metrics = {
            "lines": len(lines),
            "lines_of_code": len([line for line in lines if line.strip() and not line.strip().startswith("#")]),
            "comments": len([line for line in lines if line.strip().startswith("#") or "//" in line]),
            "blank_lines": len([line for line in lines if not line.strip()]),
        }
        
        # Calculate complexity
        metrics["complexity"] = calculate_complexity_metrics(root_node, language)
        
        return metrics
    
    def _determine_purpose(self, source_code: str, root_node: Node, language: str) -> str:
        """
        Determine the main purpose of the file.
        
        This is a simplified analysis - in production, this would use
        more sophisticated pattern matching and ML techniques.
        """
        filename = Path(source_code).name if hasattr(source_code, 'name') else "unknown"
        
        # Common file purpose patterns
        purpose_patterns = {
            "main_program": [
                r"def main\(", r"if __name__ == .__main__.", r"main\(",
                r"public static void main", r"int main\(",
            ],
            "library_module": [
                r"^class\s+\w+", r"^def\s+\w+", r"^function\s+\w+",
                r"^export\s+", r"^module\.exports",
            ],
            "configuration": [
                r"config", r"settings", r"\.env", r"\.ini", r"\.cfg",
            ],
            "test_file": [
                r"test_", r"_test", r"Test", r"spec", r"Spec",
            ],
            "data_model": [
                r"class.*Model", r"struct\s+\w+", r"interface\s+\w+",
            ],
            "utility_functions": [
                r"utils", r"utilities", r"helper", r"tools",
            ],
        }
        
        # Check patterns
        for purpose, patterns in purpose_patterns.items():
            for pattern in patterns:
                if re.search(pattern, source_code, re.IGNORECASE):
                    return purpose
        
        # Default classification based on content
        if len(source_code.split("\n")) < 50:
            return "simple_script"
        elif "class" in source_code or "def " in source_code or "function" in source_code:
            return "library_module"
        else:
            return "configuration"
    
    def _analyze_structure(self, root_node: Node, source_code: str, language: str) -> dict[str, Any]:
        """Analyze the overall structure of the code."""
        structure = {
            "has_classes": False,
            "has_functions": False,
            "has_imports": False,
            "has_comments": False,
            "is_object_oriented": False,
            "is_functional": False,
            "is_procedural": False,
        }
        
        # Count different node types
        node_counts = {}
        
        def count_nodes(node: Node):
            node_type = node.type
            node_counts[node_type] = node_counts.get(node_type, 0) + 1
            
            for child in node.children:
                count_nodes(child)
        
        count_nodes(root_node)
        
        # Determine structure based on node counts
        structure["has_classes"] = node_counts.get("class_declaration", 0) > 0 or \
                                   node_counts.get("class_definition", 0) > 0
        structure["has_functions"] = node_counts.get("function_definition", 0) > 0 or \
                                     node_counts.get("method_declaration", 0) > 0
        structure["has_imports"] = node_counts.get("import_statement", 0) > 0 or \
                                   node_counts.get("import_from_statement", 0) > 0
        structure["has_comments"] = node_counts.get("comment", 0) > 0
        
        # Determine programming paradigm
        if structure["has_classes"]:
            structure["is_object_oriented"] = True
        if structure["has_functions"] and not structure["has_classes"]:
            structure["is_functional"] = True
        if not structure["has_classes"] and not structure["has_functions"]:
            structure["is_procedural"] = True
        
        structure["node_counts"] = node_counts
        
        return structure
    
    def _extract_dependencies(self, root_node: Node, source_code: str, language: str) -> list[str]:
        """Extract dependencies and imports from the code."""
        dependencies = []
        
        # Language-specific import extraction
        if language == "python":
            # Extract Python imports
            import_pattern = r"^(?:import|from)\s+(\w+)"
            for line in source_code.split("\n"):
                match = re.match(import_pattern, line.strip())
                if match:
                    dependencies.append(match.group(1))
        
        elif language == "javascript":
            # Extract JavaScript/Node.js imports
            import_patterns = [
                r"import\s+.*?\s+from\s+['\"]([^'\"]+)['\"]",
                r"require\s*\(\s*['\"]([^'\"]+)['\"]",
                r"const\s+\w+\s*=\s*require\s*\(\s*['\"]([^'\"]+)['\"]",
            ]
            for pattern in import_patterns:
                matches = re.findall(pattern, source_code)
                dependencies.extend(matches)
        
        elif language == "java":
            # Extract Java imports
            java_import_pattern = r"import\s+([\w.]+)"
            matches = re.findall(java_import_pattern, source_code)
            dependencies.extend(matches)
        
        # Remove duplicates and sort
        return sorted(list(set(dependencies)))
    
    def _extract_functions(self, root_node: Node, source_code: str, language: str) -> list[dict[str, Any]]:
        """Extract function/method information."""
        functions = []
        
        # This is a simplified version - in production, you'd traverse the AST
        # to properly extract function information
        
        if language == "python":
            # Extract Python functions
            function_pattern = r"def\s+(\w+)\s*\((.*?)\):"
            for match in re.finditer(function_pattern, source_code):
                func_name = match.group(1)
                params = match.group(2).strip()
                
                functions.append({
                    "name": func_name,
                    "parameters": [p.strip() for p in params.split(",")] if params else [],
                    "line_number": source_code[:match.start()].count("\n") + 1,
                })
        
        elif language == "javascript":
            # Extract JavaScript functions
            function_patterns = [
                r"function\s+(\w+)\s*\((.*?)\)",
                r"const\s+(\w+)\s*=\s*\((.*?)\)\s*=>",
                r"(\w+)\s*=\s*function\s*\((.*?)\)",
            ]
            
            for pattern in function_patterns:
                for match in re.finditer(pattern, source_code):
                    func_name = match.group(1)
                    params = match.group(2).strip() if match.group(2) else ""
                    
                    functions.append({
                        "name": func_name,
                        "parameters": [p.strip() for p in params.split(",")] if params else [],
                        "line_number": source_code[:match.start()].count("\n") + 1,
                    })
        
        return functions
    
    def _extract_classes(self, root_node: Node, source_code: str, language: str) -> list[dict[str, Any]]:
        """Extract class information."""
        classes = []
        
        if language == "python":
            # Extract Python classes
            class_pattern = r"class\s+(\w+)(?:\s*\((.*?)\))?\s*:"
            for match in re.finditer(class_pattern, source_code):
                class_name = match.group(1)
                parent_classes = match.group(2).strip() if match.group(2) else ""
                
                classes.append({
                    "name": class_name,
                    "inherits": [p.strip() for p in parent_classes.split(",")] if parent_classes else [],
                    "line_number": source_code[:match.start()].count("\n") + 1,
                })
        
        elif language in ["java", "javascript", "typescript"]:
            # Extract Java/JavaScript/TypeScript classes
            class_pattern = r"class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([\w,\s]+))?\s*\{"
            for match in re.finditer(class_pattern, source_code):
                class_name = match.group(1)
                extends = match.group(2) or ""
                implements = match.group(3) or ""
                
                inherits = []
                if extends:
                    inherits.append(extends.strip())
                if implements:
                    inherits.extend([i.strip() for i in implements.split(",")])
                
                classes.append({
                    "name": class_name,
                    "inherits": inherits,
                    "line_number": source_code[:match.start()].count("\n") + 1,
                })
        
        return classes
    
    def _analyze_without_parser(self, file_path: Path, source_code: str, language: str) -> dict[str, Any]:
        """
        Analyze a file without tree-sitter parser (fallback method).
        
        Args:
            file_path: Path to the file
            source_code: Content of the file
            language: Detected language
            
        Returns:
            Basic analysis results
        """
        return {
            "file_path": str(file_path),
            "filename": file_path.name,
            "language": language,
            "size": len(source_code),
            "metrics": self._extract_metrics(source_code, None, language),
            "purpose": self._determine_purpose(source_code, None, language),
            "structure": {"has_parser": False},
            "dependencies": [],
            "functions": [],
            "classes": [],
        }