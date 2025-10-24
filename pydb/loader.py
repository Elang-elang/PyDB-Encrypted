import json
import os
from typing import Optional, Dict, Any, Union, List
from .encrypted import load
from .PyDB import Database, Table, Column


class loader:
    """
    Class untuk memuat file database PyDB dengan output terstruktur
    
    Format output:
    {
        "name": "nama_database",
        "tables": {
            "nama_tabel": {
                "columns": { ... },
                "data": [ ... ]
            }
        }
    }
    """
    
    def __init__(
        self, 
        path: str, 
        password: str, 
        json_output: bool = True,  # Default True untuk format terstruktur
        enable_filter: bool = False, 
        debug_mode: bool = False,
    ):
        """
        Inisialisasi loader database PyDB
        
        Args:
            path: Path file database (.pydb)
            password: Password untuk dekripsi
            json_output: Jika True, output dalam format JSON terstruktur
            enable_filter: Jika True, aktifkan filtering data
            debug_mode: Jika True, tampilkan info debug
        """
        self._validate_initialization(path, password, json_output, enable_filter)
        
        self.path = os.path.abspath(path)
        self.password = password
        self.json_output = json_output
        self.enable_filter = enable_filter
        self.debug_mode = debug_mode
        
        # Cache untuk data yang sudah dimuat
        self._loaded_data = None
        self._structured_data = None
    
    def _validate_initialization(self, path: str, password: str, json_output: bool, enable_filter: bool) -> None:
        """
        Validasi parameter inisialisasi
        """
        if not isinstance(path, str):
            raise TypeError("Path harus berupa string")
        
        if not isinstance(password, str) or not password:
            raise ValueError("Password harus berupa string tidak kosong")
        
        if not isinstance(json_output, bool):
            raise TypeError("json_output harus boolean")
        
        if not isinstance(enable_filter, bool):
            raise TypeError("enable_filter harus boolean")
        
        # Validasi file existence dan extension
        if not os.path.exists(path):
            raise FileNotFoundError(f"File tidak ditemukan: {path}")
        
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Path harus berupa file: {path}")
        
        if not path.endswith(".pydb"):
            raise ValueError("File harus berformat .pydb")
        
        # Validasi kombinasi parameter
        if enable_filter and not json_output:
            raise ValueError("Filter membutuhkan JSON output diaktifkan")
    
    def _load_raw_data(self) -> str:
        """
        Memuat data mentah dari file terenkripsi
        
        Returns:
            String data yang sudah didekripsi
        """
        try:
            return load(self.password, self.path)
        except Exception as e:
            raise Exception(f"Gagal memuat data dari {self.path}: {e}")
    
    def _parse_to_structured_format(self, raw_data: str) -> Dict[str, Any]:
        """
        Parse data mentah ke format terstruktur PyDB
        
        Args:
            raw_data: Data mentah dari file
            
        Returns:
            Data dalam format terstruktur PyDB
        """
        try:
            # Parse string ke dictionary
            data_dict = json.loads(raw_data)
            
            # Validasi struktur dasar
            if not isinstance(data_dict, dict):
                raise ValueError("Data tidak dalam format dictionary")
            
            # Pastikan struktur sesuai format PyDB
            structured_data = {
                "name": data_dict.get("name", ""),
                "tables": {}
            }
            
            # Process tables
            tables_data = data_dict.get("tables", {})
            if not isinstance(tables_data, dict):
                raise ValueError("Struktur tables tidak valid")
            
            for table_name, table_info in tables_data.items():
                if isinstance(table_info, dict):
                    structured_data["tables"][table_name] = {
                        "data": table_info.get("data", [None])
                    }
            
            return structured_data
            
        except Exception as e:
            raise ValueError(f"Gagal parsing data ke format terstruktur: {e}")
    
    def _load_structured_data(self) -> Dict[str, Any]:
        """
        Memuat data dalam format terstruktur PyDB
        
        Returns:
            Data terstruktur sesuai format PyDB
        """
        if self._structured_data is None:
            raw_data = self._load_raw_data()
            self._structured_data = self._parse_to_structured_format(raw_data)
        return self._structured_data
    
    def _filter_database_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Filter data database untuk output yang bersih
        
        Args:
            data: Data database lengkap
            
        Returns:
            Data yang sudah difilter
        """
        if self.debug_mode:
            # Debug mode: return semua data termasuk auto_increment dll
            return data
        
        # Filter mode: hanya data essensial
        filtered_data = {
            "name": data.get("name", ""),
            "tables": {}
        }
        
        for table_name, table_info in data.get("tables", {}).items():
            filtered_data["tables"][table_name] = {
                "data": table_info.get("data", [None])
            }
        
        return filtered_data
    
    def get_database_name(self) -> str:
        """
        Mendapatkan nama database
        
        Returns:
            Nama database
        """
        structured_data = self._load_structured_data()
        return structured_data.get("name", "")
    
    def get_table_names(self) -> List[str]:
        """
        Mendapatkan daftar nama tabel dalam database
        
        Returns:
            List nama tabel
        """
        structured_data = self._load_structured_data()
        return list(structured_data.get("tables", {}).keys())
    
    def get_table_info(self, table_name: str) -> Optional[Dict[str, Any]]:
        """
        Mendapatkan informasi tabel spesifik
        
        Args:
            table_name: Nama tabel
            
        Returns:
            Informasi tabel atau None jika tidak ditemukan
        """
        structured_data = self._load_structured_data()
        tables = structured_data.get("tables", {})
        
        if table_name in tables:
            return tables[table_name]
        
        return None
    
    def get_table_data(self, table_name: str) -> Optional[List[Dict[str, Any]]]:
        """
        Mendapatkan data dari tabel spesifik
        
        Args:
            table_name: Nama tabel
            
        Returns:
            List data tabel atau None jika tidak ditemukan
        """
        table_info = self.get_table_info(table_name)
        if table_info:
            return table_info.get("data", [])
        return None
    
    def get_table_columns(self, table_name: str) -> Optional[Dict[str, Any]]:
        """
        Mendapatkan definisi kolom dari tabel spesifik
        
        Args:
            table_name: Nama tabel
            
        Returns:
            Definisi kolom atau None jika tidak ditemukan
        """
        table_info = self.get_table_info(table_name)
        if table_info:
            return table_info.get("columns", {})
        return None
    
    def get_column_names(self, table_name: str) -> Optional[List[str]]:
        """
        Mendapatkan daftar nama kolom dari tabel spesifik
        
        Args:
            table_name: Nama tabel
            
        Returns:
            List nama kolom atau None jika tidak ditemukan
        """
        columns = self.get_table_columns(table_name)
        if columns:
            return list(columns.keys())
        return None
    
    def _process_output(self) -> Union[str, Dict[str, Any]]:
        """
        Memproses output berdasarkan konfigurasi
        
        Returns:
            Data yang sudah diproses sesuai konfigurasi
        """
        if not self.json_output:
            # Return raw data sebagai string
            return self._load_raw_data()
        
        # Get structured data
        structured_data = self._load_structured_data()
        
        if self.enable_filter:
            # Apply filtering
            return self._filter_database_data(structured_data)
        else:
            # Return full structured data
            return structured_data
    
    def load(self) -> Dict[str, Any]:
        """
        Memuat data database dalam format terstruktur
        
        Returns:
            Data database dalam format:
            {
                "name": "nama_database",
                "tables": {
                    "nama_tabel": {
                        "columns": { ... },
                        "data": [ ... ]
                    }
                }
            }
        
        Example:
            >>> db_loader = loader("database.pydb", "password123")
            >>> data = db_loader.load()
            >>> print(data["name"])  # Nama database
            >>> print(data["tables"]["users"]["data"])  # Data tabel users
        """
        result = self._process_output()
        
        # Ensure we always return the structured format
        if isinstance(result, str):
            # If raw string, parse to structured format
            return self._parse_to_structured_format(result)
        
        return result
    
    def get_database_summary(self) -> Dict[str, Any]:
        """
        Mendapatkan summary database
        
        Returns:
            Dictionary berisi summary database
        """
        structured_data = self._load_structured_data()
        
        table_count = len(structured_data.get("tables", {}))
        total_records = 0
        table_info = {}
        
        for table_name, table_data in structured_data.get("tables", {}).items():
            record_count = len(table_data.get("data", []))
            column_count = len(table_data.get("columns", {}))
            total_records += record_count
            
            table_info[table_name] = {
                "records": record_count,
                "columns": column_count
            }
        
        return {
            "name": structured_data.get("name", ""),
            "table_count": table_count,
            "total_records": total_records,
            "tables": table_info,
            "file_path": self.path
        }
    
    def validate_database(self) -> bool:
        """
        Validasi integritas database
        
        Returns:
            True jika database valid
        """
        try:
            structured_data = self._load_structured_data()
            
            # Validasi struktur dasar
            if not isinstance(structured_data, dict):
                return False
            
            if "name" not in structured_data or "tables" not in structured_data:
                return False
            
            # Validasi tables
            tables = structured_data["tables"]
            if not isinstance(tables, dict):
                return False
            
            for table_name, table_info in tables.items():
                if not isinstance(table_info, dict):
                    return False
                if "columns" not in table_info or "data" not in table_info:
                    return False
                if not isinstance(table_info["columns"], dict):
                    return False
                if not isinstance(table_info["data"], list):
                    return False
            
            return True
            
        except Exception:
            return False
    
    @property
    def value(self) -> Dict[str, Any]:
        """
        Property untuk kompatibilitas - return data terstruktur
        
        Returns:
            Data database terstruktur
        """
        return self.load()
    
    def __repr__(self) -> str:
        """
        Representasi string dari object
        """
        return (
            f"loader("
            f"path='{self.path}', "
            f"password='{'*' * len(self.password)}', "
            f"json_output={self.json_output}, "
            f"enable_filter={self.enable_filter}, "
            f"debug_mode={self.debug_mode})"
        )
    
    def __str__(self) -> str:
        """
        String representation untuk user
        """
        summary = self.get_database_summary()
        return (
            f"Database: {summary['name']}\n"
            f"Tables: {summary['table_count']}\n"
            f"Total Records: {summary['total_records']}\n"
            f"File: {self.path}"
        )


# Import ast untuk literal_eval



# Contoh penggunaan
def contoh_penggunaan():
    """Contoh penggunaan loader"""
    
    try:
        # Contoh 1: Load data terstruktur (default)
        db_loader = loader("database.pydb", "password123")
        data = db_loader.load()
        
        print("Nama Database:", data["name"])
        print("Tabel tersedia:", list(data["tables"].keys()))
        
        # Akses data tabel users
        if "users" in data["tables"]:
            users_data = data["tables"]["users"]["data"]
            users_columns = data["tables"]["users"]["columns"]
            print(f"Data users: {len(users_data)} records")
            print(f"Kolom users: {list(users_columns.keys())}")
        
        # Contoh 2: Mendapatkan summary
        summary = db_loader.get_database_summary()
        print("\nSummary Database:")
        print(f"  Nama: {summary['name']}")
        print(f"  Jumlah Tabel: {summary['table_count']}")
        print(f"  Total Record: {summary['total_records']}")
        
        # Contoh 3: Akses data spesifik
        table_names = db_loader.get_table_names()
        print(f"\nDaftar Tabel: {table_names}")
        
        for table_name in table_names:
            columns = db_loader.get_column_names(table_name)
            data_count = len(db_loader.get_table_data(table_name) or [])
            print(f"  - {table_name}: {len(columns or [])} kolom, {data_count} data")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    contoh_penggunaan()