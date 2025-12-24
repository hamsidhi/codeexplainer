from typing import Any
"""Language parsers for CodeExplainer."""

from .tree_sitter_parsers import (
    get_parser_for_language,
    get_language_mapping,
    initialize_parsers,
)

__all__ = ["get_parser_for_language", "get_language_mapping", "initialize_parsers"]