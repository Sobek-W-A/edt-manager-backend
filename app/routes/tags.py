"""
This module contains the Tag TypedDict.
"""
from typing import TypedDict

# This represents a tag.
Tag = TypedDict("Tag", {"name": str, "description": str})
