__version__ = "1.0.0"

from .core import FileRenamer
from .patterns import (
    add_prefix,
    add_suffix,
    replace_text,
    number_sequence,
    change_case,
    date_time_name,
)

__all__ = [
    "FileRenamer",
    "add_prefix",
    "add_suffix",
    "replace_text",
    "number_sequence",
    "change_case",
    "date_time_name",
]
