from .PyDB import Database, Table, ColumnDefinition as Column
from .encrypted import decrypt, encrypt, save, load
 
class Encrypted:
    encrypt = encrypt
    decrypt = decrypt
    save_to_file = save
    load_from_file = load
    
 class pydb:
     Database = Database
     Table = Table
     Column = Column
 
__all__ = [
    'pydb'
    'Encrypted',
]