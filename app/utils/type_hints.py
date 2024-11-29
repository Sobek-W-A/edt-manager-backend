"""
This module is used to provide several Type Aliases to make typing easier.
"""

from typing import Mapping, TypeAlias, Union


JsonType: TypeAlias = Union[str, int, float, bool, None,
                            Mapping[str, 'JsonType'],
                            list['JsonType']]
