# PyDB - Encrypted Python Database

## English

### Introduction

**PyDB** is a simple, efficient, and encrypted Python database library for storing data ranging from small to massive scale. This is an open-source database solution that uses JSON-based storage with encryption to keep your data secure.

### Key Features

- **Encrypted Storage**: All data is encrypted using password-based encryption
- **Simple API**: Easy-to-use interface for database operations
- **Type Safety**: Column definitions with data type validation
- **CRUD Operations**: Full support for Create, Read, Update, and Delete operations
- **Lightweight**: No external database server required
- **Python Native**: Pure Python implementation

### Basic Usage

```python
from pydb import (
    # Configurate
    Database, Column,
    
    # Type
    String, Number, Integer, Float, Boolean
)
# Create a new encrypted database
db = Database.create_new(
    "my_database.pydb", # file.pydb
    "my_password", # a password
)

# Define table columns
columns = {
    'id': Column('id', Integer, nullable=False),
    'name': Column('name', String, max_length=100),
    'email': Column('email', String)
}

# Create table and insert data
table = db.create_table("users", columns)
table.insert_data(id=1, name="John", email="john@example.com")

# Save database
db.save()
```

### Author

**Elang Muhammad R. J. (Elang-elang)**

### License

This project is licensed under the MIT License. If you modify or improve this code, please contact the author or include attribution and update the repository.

### Note

This database is based on encrypted JSON storage. While you can create similar databases from scratch or modify this script, databases created using similar concepts are considered derivative works and should maintain proper attribution.

---

## Bahasa Indonesia

### Perkenalan

**PyDB** adalah library database Python yang sederhana, efisien, dan terenkripsi untuk menyimpan data dari skala kecil hingga masif. Ini adalah solusi database open-source yang menggunakan penyimpanan berbasis JSON dengan enkripsi untuk menjaga keamanan data Anda.

### Fitur Utama

- **Penyimpanan Terenkripsi**: Semua data dienkripsi menggunakan enkripsi berbasis kata sandi
- **API Sederhana**: Interface yang mudah digunakan untuk operasi database
- **Keamanan Tipe Data**: Definisi kolom dengan validasi tipe data
- **Operasi CRUD**: Dukungan penuh untuk operasi Create, Read, Update, dan Delete
- **Ringan**: Tidak memerlukan server database eksternal
- **Native Python**: Implementasi murni Python

### Penggunaan Dasar

```python
from PyDB import (
    # Configurasi
    Database, Column,
    
    # Tipe
    String, Number, Integer, Float, Boolean
)
# Buat database terenkripsi baru
db = Database.create_new(
    "database_saya.pydb", # file.pydb
    "kata_sandi_saya" # kata sandi
)

# Definisikan kolom tabel
columns = {
    'id': Column('id', int, nullable=False),
    'nama': Column('nama', str, max_length=100),
    'email': Column('email', str)
}

# Buat tabel dan masukkan data
table = db.create_table("pengguna", columns)
table.insert_data(id=1, nama="John", email="john@example.com")

# Simpan database
db.save()
```

### Pembuat

**Elang Muhammad R. J. (Elang-elang)**

### Lisensi

Proyek ini dilisensikan di bawah MIT License. Jika Anda memodifikasi atau memperbaiki kode ini, harap hubungi pembuat atau sertakan atribusi dan perbarui repositori.

### Catatan

Database ini didasarkan pada penyimpanan JSON terenkripsi. Meskipun Anda dapat membuat database serupa dari awal atau memodifikasi script ini, database yang dibuat menggunakan konsep serupa dianggap sebagai karya turunan dan harus mempertahankan atribusi yang tepat.

---

## Installation

```bash
pip install PyDB-Encrypted
```

## Requirements

- Python 3.7+
- cryptography

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions or contributions, please contact Elang Muhammad R. J. (Elang-elang)