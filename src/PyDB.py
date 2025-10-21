import os
import ast
import copy
import json
import base64
from typing import Dict, List, Any, Optional, Union, Callable, Tuple
from enum import Enum
from datetime import datetime
from .encrypted import TextEncryptor, encrypt, decrypt, save, load

# =============================================================================
# EXCEPTION CLASSES
# =============================================================================

class DatabaseError(SyntaxError):
    def __init__(self, ErrorText):
        self.ErrorText = ErrorText
        super().__init__(ErrorText)
    def __repr__(self):
        return f"DatabaseError({ErrorText})"

class DatabaseLengthError(DatabaseError, IndexError):
    def __init__(self, ErrorText):
        self.ErrorText = ErrorText
        super().__init__(ErrorText)
    def __repr__(self):
        return f"DatabaseLengthError({ErrorText})"

class DatabaseColumnError(DatabaseError, IndexError):
    def __init__(self, ErrorText):
        self.ErrorText = ErrorText
        super().__init__(ErrorText)
    def __repr__(self):
        return f"DatabaseColumnError({ErrorText})"

class DatabaseTypeError(DatabaseError, TypeError):
    def __init__(self, ErrorText):
        self.ErrorText = ErrorText
        super().__init__(ErrorText)
    def __repr__(self):
        return f"DatabaseTypeError({ErrorText})"

class DatabaseTableError(DatabaseError, IndexError, TypeError):
    def __init__(self, ErrorText):
        self.ErrorText = ErrorText
        super().__init__(ErrorText)
    def __repr__(self):
        return f"DatabaseTableError({ErrorText})"

class DatabaseValidationError(DatabaseError, ValueError):
    def __init__(self, ErrorText):
        self.ErrorText = ErrorText
        super().__init__(ErrorText)
    def __repr__(self):
        return f"DatabaseValidationError({ErrorText})"

class DatabasePathError(FileNotFoundError):
    def __init__(self, ErrorText):
        self.ErrorText = ErrorText
        super().__init__(ErrorText)
    def __repr__(self):
        return f"DatabasePathError({ErrorText})"

class PasswordValueError(DatabaseError, ValueError):
    def __init__(self, ErrorText):
        self.ErrorText = ErrorText
        super().__init__(ErrorText)
    def __repr__(self):
        return f"PasswordValueError({ErrorText})"

# =============================================================================
# ENUM FOR DATA TYPES
# =============================================================================

class DataType(Enum):
    """Enum untuk tipe data yang didukung"""
    STRING = str
    INTEGER = int 
    FLOAT = float
    BOOLEAN = bool
    NONE = type(None)
    
    @classmethod
    def get_supported_types(cls) -> Tuple[type, ...]:
        """Mengembalikan tuple dari tipe data yang didukung"""
        return (str, (int, float), int, float, bool, type(None))

# =============================================================================
# COLUMN DEFINITION CLASS
# =============================================================================

class Column:
    """
    Kelas untuk mendefinisikan kolom dengan tipe data dan constraint
    """
    
    def __init__(
        self, 
        name: str, 
        data_type: type,
        min_length: int = 0,
        max_length: int = 0,
        nullable: bool = True,
        default_value: Any = None
    ):
        # Validasi parameter dasar
        if not isinstance(name, str) or not name.strip():
            raise DatabaseColumnError("Nama kolom harus string tidak kosong")
        
        if data_type not in DataType.get_supported_types():
            raise DatabaseTypeError(f"Tipe data tidak didukung: {data_type}")
        
        if min_length < 0:
            raise DatabaseLengthError("Panjang minimal tidak boleh negatif")
        
        if max_length < 0:
            raise DatabaseLengthError("Panjang maksimal tidak boleh negatif")
        
        if min_length > max_length and max_length != 0:
            raise DatabaseLengthError(
                f"Panjang minimal ({min_length}) tidak boleh lebih besar dari panjang maksimal ({max_length})"
            )
        
        # Set atribut
        self.name = name.strip()
        self.data_type = data_type
        self.min_length = min_length
        self.max_length = max_length
        self.nullable = nullable
        self.default_value = default_value
        
        # Validasi default value
        if default_value is not None:
            if not self._validate_single_value(default_value):
                raise DatabaseValidationError(
                    f"Nilai default tidak valid untuk kolom {self.name}"
                )

    def _validate_single_value(self, value: Any) -> bool:
        """Validasi nilai tunggal berdasarkan constraint kolom"""
        try:
            # Cek nullability
            if value is None:
                return self.nullable
            
            # Cek tipe data
            if not isinstance(value, self.data_type):
                return False
            
            # Validasi panjang untuk string
            if self.data_type == str:
                length = len(value)
                if self.max_length > 0 and length > self.max_length:
                    return False
                if length < self.min_length:
                    return False
            
            # Validasi range untuk numerik
            elif self.data_type in (int, float):
                if self.max_length > 0 and value > self.max_length:
                    return False
                if value < self.min_length:
                    return False
            
            return True
            
        except Exception:
            return False

    def validate_value(self, value: Any) -> bool:
        """Validasi nilai (publik interface)"""
        return self._validate_single_value(value)
    
    def get_default_value(self) -> Any:
        """Mengembalikan nilai default yang sudah divalidasi"""
        if self.default_value is not None:
            return self.default_value
        return None if self.nullable else self._get_type_default()
    
    def _get_type_default(self) -> Any:
        """Mengembalikan nilai default berdasarkan tipe data"""
        type_defaults = {
            str: "",
            int: 0,
            float: 0.0,
            bool: False,
            type(None): None
        }
        return type_defaults.get(self.data_type, None)
    
    def __repr__(self) -> str:
        length = ""
        if self.max_length and self.min_length:
            length = { "min_length": self.min_length, "max_length": self.max_length }
            length = f", length={length}"
            
        return f"Column(name='{self.name}', type={"number" if isinstance(self.data_type, (list, tuple)) else self.data_type.__name__)}{length if length else ""}, nullable={self.nullable}, default_value={self.default_value if ((self.default_value is not None) or (self.default_value)) else '""'})"

# =============================================================================
# TABLE CLASS
# =============================================================================

class Table:
    """
    Kelas untuk representasi tabel dalam database
    """
    
    def __init__(self, name: str, columns: Dict[str, Column]):
        # Validasi nama tabel
        if not isinstance(name, str) or not name.strip():
            raise DatabaseTableError("Nama tabel harus string tidak kosong")
        
        # Validasi kolom
        if not columns or not isinstance(columns, dict):
            raise DatabaseColumnError("Tabel harus memiliki minimal satu kolom")
        
        for col_name, col_def in columns.items():
            if not isinstance(col_def, Column):
                raise DatabaseColumnError("Semua kolom harus instance Column")
        
        self.name = name.strip()
        self.columns = columns.copy()
        self.data: List[Dict[str, Any]] = []
        self._auto_increment = 1
        self._created_at = datetime.now()
    
    def _validate_row_data(self, row_data: Dict[str, Any]) -> bool:
        """
        Validasi data baris sebelum dimasukkan
        """
        try:
            for col_name, value in row_data.items():
                if col_name not in self.columns:
                    return False
                
                col_def = self.columns[col_name]
                if not col_def.validate_value(value):
                    return False
            
            return True
            
        except Exception:
            return False
    
    def _apply_defaults(self, row_data: Dict[str, Any]) -> Dict[str, Any]:
        """Menerapkan nilai default untuk kolom yang tidak disediakan"""
        complete_data = row_data.copy()
        
        for col_name, col_def in self.columns.items():
            if col_name not in complete_data:
                complete_data[col_name] = col_def.get_default_value()
        
        return complete_data
    
    # =========================================================================
    # CRUD OPERATIONS
    # =========================================================================
    
    def insert_data(self, **data) -> int:
        """
        Menyisipkan data baru ke dalam tabel
        """
        # Auto increment untuk primary key jika ada kolom 'id'
        if 'id' in self.columns and 'id' not in data:
            data['id'] = self._auto_increment
            self._auto_increment += 1
        
        # Terapkan nilai default
        complete_data = self._apply_defaults(data)
        
        # Validasi data
        if not self._validate_row_data(complete_data):
            raise DatabaseValidationError(f"Validasi data gagal untuk tabel {self.name}")
        
        self.data.append(complete_data.copy())
        return complete_data.get('id', len(self.data))
    
    # Alias untuk insert_data
    tambah_data = insert_data
    
    def select_data(
        self, 
        condition: Optional[Callable[[Dict[str, Any]], bool]] = None,
        columns: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Memilih data dari tabel dengan kondisi opsional
        """
        filtered_data = self.data.copy()
        
        # Terapkan kondisi jika ada
        if condition is not None:
            filtered_data = [row for row in filtered_data if condition(row)]
        
        # Pilih kolom tertentu jika diminta
        if columns is not None:
            result = []
            for row in filtered_data:
                selected_row = {}
                for col in columns:
                    if col in row:
                        selected_row[col] = row[col]
                result.append(selected_row)
            return result
        
        return filtered_data
    
    # Alias untuk select_data
    ambil_data = select_data
    
    def update_data(
        self, 
        condition: Callable[[Dict[str, Any]], bool], 
        **updates
    ) -> int:
        """
        Memperbarui data berdasarkan kondisi
        """
        updated_count = 0
        
        for row in self.data:
            if condition(row):
                # Buat salinan sementara untuk validasi
                temp_row = row.copy()
                temp_row.update(updates)
                
                # Validasi data yang diupdate
                if self._validate_row_data(temp_row):
                    row.update(updates)
                    updated_count += 1
                else:
                    raise DatabaseValidationError(f"Validasi update gagal untuk data di tabel {self.name}")
        
        return updated_count
    
    # Alias untuk update_data
    perbarui_data = update_data
    
    def delete_data(self, condition: Callable[[Dict[str, Any]], bool]) -> int:
        """
        Menghapus data berdasarkan kondisi
        """
        initial_count = len(self.data)
        self.data = [row for row in self.data if not condition(row)]
        return initial_count - len(self.data)
    
    # Alias untuk delete_data
    hapus_data = delete_data
    
    # =========================================================================
    # UTILITY METHODS
    # =========================================================================
    
    def get_table_info(self) -> Dict[str, Any]:
        """Mengembalikan informasi tabel"""
        return {
            'name': self.name,
            'column_count': len(self.columns),
            'data_count': len(self.data),
            'columns': {name: str(col_def) for name, col_def in self.columns.items()},
            'created_at': self._created_at.isoformat()
        }
    
    def get_column_names(self) -> List[str]:
        """Mengembalikan daftar nama kolom"""
        return list(self.columns.keys())
    
    def count_data(self, condition: Optional[Callable[[Dict], bool]] = None) -> int:
        """Menghitung jumlah data yang memenuhi kondisi"""
        if condition is None:
            return len(self.data)
        return len([row for row in self.data if condition(row)])
    
    def __repr__(self) -> str:
        return f"Table(name='{self.name}', columns={len(self.columns)}, data={len(self.data)})"

# =============================================================================
# DATABASE CLASS WITH ENCRYPTION
# =============================================================================

class Database:
    """
    Kelas utama untuk manajemen database dengan enkripsi
    """
    
    def __init__(self, name: str, password: str, storage_path: str = "MyPyDB.pydb", create_new: bool = False):
        """
        Inisialisasi database dengan password
        
        Args:
            name: Nama database
            password: Password untuk enkripsi/dekripsi
            storage_path: Path penyimpanan
            create_new: True untuk membuat database baru (overwrite jika ada)
        """
        # Validasi parameter
        if not isinstance(name, str) or not name.strip():
            raise DatabaseError("Nama database harus string tidak kosong")
        
        if not name.endswith(".pydb"):
            name += ".pydb"
            
        if not password:
            raise PasswordValueError("Password harus disediakan")
        
        storage_path = str(os.path.abspath(storage_path))
        
        if not isinstance(storage_path, str) or not storage_path.strip():
            raise DatabasePathError("Path penyimpanan harus string tidak kosong")
        
        # Cek dan buat path jika tidak ada
        if not os.path.exists(storage_path):
            try:
                os.makedirs(storage_path, exist_ok=True)
            except Exception as e:
                raise DatabasePathError(f"Tidak dapat membuat path: {e}")
        
        if not os.access(storage_path, os.W_OK):
            raise DatabasePathError(f"Path tidak dapat ditulisi: {storage_path}")
        
        self.name = name.strip()
        self.password = password
        self.storage_path = storage_path
        self.tables: Dict[str, Table] = {}
        self.file_path = str(os.path.join(storage_path, self.name))
        
        # Muat data yang ada atau buat baru
        if create_new:
            self._create_new_database()
        elif not create_new or create_new and os.path.exists(storage_path):
            self._load_from_file()
    
    def _create_new_database(self):
        """Buat database baru"""
        self.tables.clear()
        self._save_to_file()
    
    def create_table(self, name: str, columns: Dict[str, Column]) -> Table:
        """
        Membuat tabel baru
        """
        if name in self.tables:
            raise DatabaseTableError(f"Tabel '{name}' sudah ada")
        
        table = Table(name, columns)
        self.tables[name] = table
        self._save_to_file()
        
        return table
    
    # Alias untuk create_table
    buat_tabel = create_table
    
    def drop_table(self, name: str) -> bool:
        """
        Menghapus tabel
        """
        if name not in self.tables:
            raise DatabaseTableError(f"Tabel '{name}' tidak ditemukan")
        
        del self.tables[name]
        self._save_to_file()
        return True
    
    # Alias untuk drop_table
    hapus_tabel = drop_table
    
    def get_table(self, name: str) -> Table:
        """
        Mendapatkan instance tabel
        """
        if name not in self.tables:
            raise DatabaseTableError(f"Tabel '{name}' tidak ditemukan")
        
        return self.tables[name]
    
    # Alias untuk get_table
    dapatkan_tabel = get_table
    
    def _serialize_to_dict(self) -> Dict[str, Any]:
        """Mengkonversi database ke dictionary untuk serialisasi"""
        serialized = {
            'name': self.name,
            'tables': {}
        }
        
        for table_name, table in self.tables.items():
            serialized['tables'][table_name] = {
                'columns': {},
                'data': table.data,
                'auto_increment': table._auto_increment
            }
            
            for col_name, col_def in table.columns.items():
                serialized['tables'][table_name]['columns'][col_name] = {
                    'data_type': col_def.data_type.__name__,
                    'min_length': col_def.min_length,
                    'max_length': col_def.max_length,
                    'nullable': col_def.nullable,
                    'default_value': col_def.default_value
                }
        
        return serialized
    
    def _deserialize_from_dict(self, data: Dict[str, Any]) -> None:
        """Mengkonversi dictionary ke database"""
        try:
            self.tables.clear()
            
            for table_name, table_data in data.get('tables', {}).items():
                # Rekonstruksi kolom
                columns = {}
                for col_name, col_def_data in table_data.get('columns', {}).items():
                    # Konversi string type ke actual type
                    type_mapping = {
                        'str': str,
                        'int': int,
                        'float': float,
                        'bool': bool,
                        'NoneType': type(None)
                    }
                    
                    data_type = type_mapping.get(col_def_data['data_type'], str)
                    
                    column_def = Column(
                        name=col_name,
                        data_type=data_type,
                        min_length=col_def_data['min_length'],
                        max_length=col_def_data['max_length'],
                        nullable=col_def_data['nullable'],
                        default_value=col_def_data['default_value']
                    )
                    columns[col_name] = column_def
                
                # Buat tabel
                table = Table(table_name, columns)
                table.data = table_data['data']
                table._auto_increment = table_data.get('auto_increment', 1)
                
                self.tables[table_name] = table
                
        except Exception as e:
            raise DatabaseError(f"Gagal memuat data database: {e}")
    
    def _save_to_file(self) -> None:
        """Menyimpan database ke file dengan enkripsi"""
        try:
            serialized_data = self._serialize_to_dict()
            data_str = json.dumps(serialized_data, indent=4)
            save(data_str, self.password, self.file_path)
        except Exception as e:
            raise DatabaseError(f"Gagal menyimpan database: {e}")
    
    def _load_from_file(self) -> None:
        """Memuat database dari file dengan dekripsi"""
        try:
            if os.path.exists(self.file_path):
                data_dict = json.loads(load(self.password, self.file_path))
                self._deserialize_from_dict(data_dict)
                    
        except PasswordValueError:
            raise PasswordValueError("Password salah atau file database korup")
        except FileNotFoundError:
            pass  # File tidak ada, database baru
        except Exception as e:
            raise DatabaseError(f"Gagal memuat database: {e}")
    
    def save(self, new_password: Optional[str] = None) -> None:
        """
        Menyimpan database dengan password baru (atau password lama)
        
        Args:
            new_password: Password baru (jika None, gunakan password lama)
        """
        if new_password:
            self.password = new_password
        self._save_to_file()
    
    def backup(self, backup_path: str, backup_password: Optional[str] = None) -> None:
        """
        Membuat backup database
        
        Args:
            backup_path: Path untuk backup
            backup_password: Password untuk backup (jika None, gunakan password saat ini)
        """
        backup_password = backup_password or self.password
        serialized_data = self._serialize_to_dict()
        data_str = str(serialized_data)
        save(data_str, backup_password, backup_path)
    
    @classmethod
    def load_from_file(cls, file_path: str, password: str) -> 'Database':
        """
        Memuat database dari file yang sudah ada
        
        Args:
            file_path: Path file database
            password: Password untuk dekripsi
            
        Returns:
            Instance Database
        """
        if not os.path.exists(file_path):
            raise DatabaseError(f"File database tidak ditemukan: {file_path}")
        
        # Ekstrak nama database dari file path
        name = os.path.splitext(os.path.basename(file_path))[0]
        storage_path = os.path.dirname(file_path)
        
        # Buat instance database
        db = cls(name, password, storage_path, create_new=False)
        return db
    
    @classmethod
    def create_new(cls, name: str, password: str, storage_path: str = ".") -> 'Database':
        """
        Membuat database baru
        
        Args:
            name: Nama database
            password: Password untuk enkripsi
            storage_path: Path penyimpanan
            
        Returns:
            Instance Database baru
        """
        return cls(name, password, storage_path, create_new=True)
    
    def get_database_info(self) -> Dict[str, Any]:
        """Mengembalikan informasi database"""
        table_info = {}
        for name, table in self.tables.items():
            table_info[name] = table.get_table_info()
        
        return {
            'name': self.name,
            'storage_path': self.storage_path,
            'file_path': self.file_path,
            'table_count': len(self.tables),
            'encrypted': True,
            'tables': table_info
        }
    
    def __repr__(self) -> str:
        return f"Database(name='{self.name}', tables={len(self.tables)}, encrypted=True)"