"""
PyDB - Encrypted Python Database
==================================

A simple, efficient, and encrypted Python database library for secure data storage.

Author: Elang Muhammad R. J. (Elang-elang)
License: MIT
"""

__version__ = "1.1.5"
__name__ = "PyDB"
__author__ = 'Elang Muhammad R. J. (Elang-elang)'
__license__ = 'MIT'

# Import main classes
from .PyDB import (
    Database,
    Table,
    Column,
    DataType,
    
    # Exceptions
    DatabaseError,
    DatabaseLengthError,
    DatabaseColumnError,
    DatabaseTypeError,
    DatabaseTableError,
    DatabaseValidationError,
    DatabasePathError,
    PasswordValueError,
)

from .encrypted import (
    encrypt,
    decrypt,
    save,
    load,
    PasswordValueError,
)

from .loader import loader

from .__type__ import String, Number, Integer, Float, Boolean

__all__ = [
    # Main classes
    'Database',
    'Table',
    'Column',
    'DataType',
    
    # Encryption utilities
    'encrypt',
    'decrypt',
    'save',
    'load',
    
    # semi/sub Encryption utilities
    'loader'
    
    # Types
    "String",
    "Number",
    "Integer",
    "Float",
    "Boolean",
    
    # Exceptions
    'DatabaseError',
    'DatabaseLengthError',
    'DatabaseColumnError',
    'DatabaseTypeError',
    'DatabaseTableError',
    'DatabaseValidationError',
    'DatabasePathError',
    'PasswordValueError',
]
