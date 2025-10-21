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
    ColumnDefinition as Column,
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

class pydb:
    Database = Database
    Table = Table
    Column = Column

class exceptions:
    DatabaseError = DatabaseError
    DatabaseLengthError = DatabaseLengthError
    DatabaseColumnError = DatabaseColumnError
    DatabaseTypeError = DatabaseTypeError
    DatabaseTableError = DatabaseTableError
    DatabaseValidationError = DatabaseValidationError
    DatabasePathError = DatabasePathError
    PasswordValueError = PasswordValueError

from .src.encrypted import (
    TextEncryptor,
    encrypt,
    decrypt,
    save,
    load,
    PasswordValueError,
)

class Encrypted:
    TextEncryptor = TextEncryptor
    dncrypt = encrypt
    decrypt = decrypt
    save = save
    load = load
    PasswordValueError = PasswordValueError

__all__ = [
    # Main classes
    'pydb'
    
    # Encryption utilities
    'Encrypted',
    
    # Exceptions
    'exceptions'
]