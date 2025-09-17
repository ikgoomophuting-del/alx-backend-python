#!/usr/bin/env python3
"""
Utility helpers for tests
"""

from typing import Any, Tuple, Mapping


def access_nested_map(nested_map: Mapping, path: Tuple[str, ...]) -> Any:
    """
    Retrieve a value from nested mapping using a sequence of keys (path).
    Raises KeyError if any key in the path is missing.
    """
    current = nested_map
    for key in path:
        current = current[key]
    return current
