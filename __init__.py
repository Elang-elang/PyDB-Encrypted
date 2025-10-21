"""
PyDB - Encrypted Python Database
==================================

A simple, efficient, and encrypted Python database library for secure data storage.

Author: Elang Muhammad R. J. (Elang-elang)
License: MIT
"""

__version__ = '0.1.0'
__author__ = 'Elang Muhammad R. J. (Elang-elang)'
__license__ = 'MIT'

# Import main classes
from .src.PyDB import (
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

from .src.encrypted import (
    encrypt,
    decrypt,
    save,
    load,
    PasswordValueError,
)

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