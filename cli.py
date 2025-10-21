import argparse
import os
import sys
import json
from typing import List, Dict, Any, Optional

# Import dari PyDB
from src.PyDB import (
    Database, Table, ColumnDefinition as Column, 
    DatabaseColumnError, DatabaseTypeError, DatabaseTableError,
    DatabaseError, PasswordValueError
)

class PyDBCLI:
    """CLI untuk mengakses PyDB dengan fitur lengkap"""
    
    def __init__(self):
        self.parser = self._create_parser()
        self.args = None
        self.db = None
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Membuat argument parser untuk CLI"""
        parser = argparse.ArgumentParser(
            description='Command Line Interface (CLI) untuk mengakses PyDB - Database dengan enkripsi password',
            epilog='Dibuat oleh Elang Muhammad Ridzqy Jamaludin',
            prog='pydb',
        )
        
        # Main commands
        subparsers = parser.add_subparsers(dest='command', help='Perintah utama')
        
        # CREATE command
        create_parser = subparsers.add_parser('create', help='Buat database atau tabel baru')
        create_subparsers = create_parser.add_subparsers(dest='create_command', help='Buat objek')
        
        # Create database
        db_parser = create_subparsers.add_parser('database', help='Buat database baru')
        db_parser.add_argument('file', type=str, help='Nama file database (.pydb)')
        db_parser.add_argument('--password', required=True, type=str, help='Password untuk database')
        db_parser.add_argument('--path', type=str, default='.', help='Path penyimpanan database')
        
        # Create table
        table_parser = create_subparsers.add_parser('table', help='Buat tabel baru')
        table_parser.add_argument('file', type=str, help='File database (.pydb)')
        table_parser.add_argument('--password', required=True, type=str, help='Password database')
        table_parser.add_argument('--name', required=True, type=str, help='Nama tabel')
        table_parser.add_argument('--columns', required=True, type=str, 
                                help='Definisi kolom dalam format JSON: \'{"nama": "string", "umur": "int"}\'')
        
        # INSERT command
        insert_parser = subparsers.add_parser('insert', help='Sisipkan data ke tabel')
        insert_parser.add_argument('file', type=str, help='File database (.pydb)')
        insert_parser.add_argument('--password', required=True, type=str, help='Password database')
        insert_parser.add_argument('--table', required=True, type=str, help='Nama tabel')
        insert_parser.add_argument('--data', required=True, type=str, 
                                 help='Data dalam format JSON: \'{"nama": "Alice", "umur": 25}\'')
        
        # SELECT command
        select_parser = subparsers.add_parser('select', help='Pilih data dari tabel')
        select_parser.add_argument('file', type=str, help='File database (.pydb)')
        select_parser.add_argument('--password', required=True, type=str, help='Password database')
        select_parser.add_argument('--table', required=True, type=str, help='Nama tabel')
        select_parser.add_argument('--columns', type=str, help='Kolom yang dipilih (pisah dengan koma)')
        select_parser.add_argument('--where', type=str, help='Kondisi filter (opsional)')
        select_parser.add_argument('--format', choices=['table', 'json', 'csv'], default='table', 
                                 help='Format output')
        
        # UPDATE command
        update_parser = subparsers.add_parser('update', help='Perbarui data dalam tabel')
        update_parser.add_argument('file', type=str, help='File database (.pydb)')
        update_parser.add_argument('--password', required=True, type=str, help='Password database')
        update_parser.add_argument('--table', required=True, type=str, help='Nama tabel')
        update_parser.add_argument('--data', required=True, type=str, 
                                 help='Data update dalam format JSON')
        update_parser.add_argument('--where', required=True, type=str, 
                                 help='Kondisi untuk data yang akan diupdate')
        
        # DELETE command
        delete_parser = subparsers.add_parser('delete', help='Hapus data dari tabel')
        delete_parser.add_argument('file', type=str, help='File database (.pydb)')
        delete_parser.add_argument('--password', required=True, type=str, help='Password database')
        delete_parser.add_argument('--table', required=True, type=str, help='Nama tabel')
        delete_parser.add_argument('--where', required=True, type=str, 
                                 help='Kondisi untuk data yang akan dihapus')
        
        # INFO command
        info_parser = subparsers.add_parser('info', help='Tampilkan informasi database/tabel')
        info_parser.add_argument('file', type=str, help='File database (.pydb)')
        info_parser.add_argument('--password', required=True, type=str, help='Password database')
        info_parser.add_argument('--table', type=str, help='Nama tabel spesifik (opsional)')
        
        # PASSWORD command
        password_parser = subparsers.add_parser('password', help='Ubah password database')
        password_parser.add_argument('file', type=str, help='File database (.pydb)')
        password_parser.add_argument('--old-password', required=True, type=str, help='Password lama')
        password_parser.add_argument('--new-password', required=True, type=str, help='Password baru')
        
        # BACKUP command
        backup_parser = subparsers.add_parser('backup', help='Buat backup database')
        backup_parser.add_argument('file', type=str, help='File database (.pydb)')
        backup_parser.add_argument('--password', required=True, type=str, help='Password database')
        backup_parser.add_argument('--backup-file', required=True, type=str, help='File backup')
        backup_parser.add_argument('--backup-password', type=str, help='Password backup (opsional)')
        
        # print(parser.__dict__)
        
        return parser
    
    def _load_database(self, file_path: str, password: str) -> Database:
        """Memuat database dari file"""
        try:
            return Database.load_from_file(file_path, password)
        except PasswordValueError:
            print("❌ Error: Password salah!")
            sys.exit(1)
        except DatabaseError as e:
            print(f"❌ Error database: {e}")
            sys.exit(1)
    
    def _parse_json_data(self, json_str: str) -> Dict[str, Any]:
        """Parse string JSON menjadi dictionary"""
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"❌ Error: Format JSON tidak valid - {e}")
            sys.exit(1)
    
    def _parse_columns_definition(self, columns_json: str) -> Dict[str, Column]:
        """Parse definisi kolom dari JSON"""
        try:
            columns_def = json.loads(columns_json)
            columns = {}
            type_mapping = {
                'string': str,
                'str': str,
                'integer': int,
                'int': int,
                'float': float,
                'boolean': bool,
                'bool': bool,
                'none': type(None)
            }
            
            for col_name, col_type in columns_def.items():
                if isinstance(col_type, str):
                    data_type = type_mapping.get(col_type.lower(), str)
                    columns[col_name] = Column(col_name, data_type)
                elif isinstance(col_type, dict):
                    # Advanced column definition
                    data_type = type_mapping.get(col_type.get('type', 'string').lower(), str)
                    columns[col_name] = Column(
                        name=col_name,
                        data_type=data_type,
                        min_length=col_type.get('min_length', 0),
                        max_length=col_type.get('max_length', 0),
                        nullable=col_type.get('nullable', True),
                        default_value=col_type.get('default_value')
                    )
            
            return columns
            
        except Exception as e:
            print(f"❌ Error: Format definisi kolom tidak valid - {e}")
            sys.exit(1)
    
    def _create_condition_function(self, where_clause: str) -> callable:
        """Membuat fungsi kondisi dari string where clause"""
        try:
            # Sederhana: asumsikan format "kolom=value"
            if '=' in where_clause:
                col, value = where_clause.split('=', 1)
                col = col.strip()
                value = value.strip()
                
                # Coba parse value sebagai number/boolean
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                elif value.isdigit():
                    value = int(value)
                elif value.replace('.', '').isdigit():
                    value = float(value)
                elif value.lower() == 'null':
                    value = None
                
                return lambda row: row.get(col) == value
            
            # Untuk kondisi yang lebih kompleks, bisa dikembangkan
            print("⚠️  Peringatan: Format WHERE sederhana, gunakan 'kolom=value'")
            return lambda row: True
            
        except Exception as e:
            print(f"❌ Error: Format WHERE tidak valid - {e}")
            sys.exit(1)
    
    def _display_table_data(self, data: List[Dict], columns: Optional[List[str]] = None):
        """Menampilkan data dalam format tabel"""
        if not data:
            print("📭 Tidak ada data")
            return
        
        # Determine columns to display
        if not columns:
            columns = list(data[0].keys())
        
        # Calculate column widths
        col_widths = {}
        for col in columns:
            col_widths[col] = max(len(str(col)), 
                                max(len(str(row.get(col, ''))) for row in data))
        
        # Print header
        header = " | ".join(f"{col:<{col_widths[col]}}" for col in columns)
        separator = "-+-".join("-" * col_widths[col] for col in columns)
        
        print(header)
        print(separator)
        
        # Print rows
        for row in data:
            row_str = " | ".join(f"{str(row.get(col, '')):<{col_widths[col]}}" for col in columns)
            print(row_str)
    
    def handle_create_database(self, args):
        """Handle perintah create database"""
        try:
            file_path = os.path.join(args.path, args.file)
            if not args.file.endswith('.pydb'):
                file_path += '.pydb'
            
            db = Database.create_new(
                name=os.path.splitext(os.path.basename(file_path))[0],
                password=args.password,
                storage_path=args.path
            )
            
            print(f"✅ Database berhasil dibuat: {file_path}")
            
        except Exception as e:
            print(f"❌ Error membuat database: {e}")
            sys.exit(1)
    
    def handle_create_table(self, args):
        """Handle perintah create table"""
        db = self._load_database(args.file, args.password)
        
        try:
            columns = self._parse_columns_definition(args.columns)
            table = db.create_table(args.name, columns)
            
            print(f"✅ Tabel '{args.name}' berhasil dibuat")
            print(f"   Kolom: {', '.join(columns.keys())}")
            
        except Exception as e:
            print(f"❌ Error membuat tabel: {e}")
            sys.exit(1)
    
    def handle_insert(self, args):
        """Handle perintah insert"""
        db = self._load_database(args.file, args.password)
        
        try:
            data = self._parse_json_data(args.data)
            table = db.get_table(args.table)
            row_id = table.insert_data(**data)
            
            print(f"✅ Data berhasil disisipkan (ID: {row_id})")
            
        except Exception as e:
            print(f"❌ Error menyisipkan data: {e}")
            sys.exit(1)
    
    def handle_select(self, args):
        """Handle perintah select"""
        db = self._load_database(args.file, args.password)
        
        try:
            table = db.get_table(args.table)
            
            # Parse columns
            columns = None
            if args.columns:
                columns = [col.strip() for col in args.columns.split(',')]
            
            # Parse condition
            condition = None
            if args.where:
                condition = self._create_condition_function(args.where)
            
            # Get data
            data = table.select_data(condition=condition, columns=columns)
            
            # Display based on format
            if args.format == 'json':
                print(json.dumps(data, indent=2, ensure_ascii=False))
            elif args.format == 'csv':
                if data:
                    cols = columns or list(data[0].keys())
                    print(','.join(cols))
                    for row in data:
                        print(','.join(str(row.get(col, '')) for col in cols))
            else:  # table format
                self._display_table_data(data, columns)
                
            print(f"\n📊 Total: {len(data)} baris")
            
        except Exception as e:
            print(f"❌ Error mengambil data: {e}")
            sys.exit(1)
    
    def handle_update(self, args):
        """Handle perintah update"""
        db = self._load_database(args.file, args.password)
        
        try:
            table = db.get_table(args.table)
            data = self._parse_json_data(args.data)
            condition = self._create_condition_function(args.where)
            
            updated_count = table.update_data(condition, **data)
            print(f"✅ {updated_count} baris berhasil diperbarui")
            
        except Exception as e:
            print(f"❌ Error memperbarui data: {e}")
            sys.exit(1)
    
    def handle_delete(self, args):
        """Handle perintah delete"""
        db = self._load_database(args.file, args.password)
        
        try:
            table = db.get_table(args.table)
            condition = self._create_condition_function(args.where)
            
            deleted_count = table.delete_data(condition)
            print(f"✅ {deleted_count} baris berhasil dihapus")
            
        except Exception as e:
            print(f"❌ Error menghapus data: {e}")
            sys.exit(1)
    
    def handle_info(self, args):
        """Handle perintah info"""
        db = self._load_database(args.file, args.password)
        
        try:
            if args.table:
                # Info tabel spesifik
                table = db.get_table(args.table)
                info = table.get_table_info()
                
                print(f"📋 Informasi Tabel: {args.table}")
                print(f"   Jumlah Kolom: {info['column_count']}")
                print(f"   Jumlah Data: {info['data_count']}")
                print(f"   Dibuat: {info['created_at']}")
                print(f"   Kolom: {', '.join(table.get_column_names())}")
                
            else:
                # Info database
                info = db.get_database_info()
                
                print(f"🏢 Informasi Database: {info['name']}")
                print(f"   Path: {info['file_path']}")
                print(f"   Jumlah Tabel: {info['table_count']}")
                print(f"   Terenkripsi: {info['encrypted']}")
                print("\n   Tabel:")
                for table_name, table_info in info['tables'].items():
                    print(f"     - {table_name}: {table_info['data_count']} data")
                    
        except Exception as e:
            print(f"❌ Error mengambil informasi: {e}")
            sys.exit(1)
    
    def handle_password(self, args):
        """Handle perintah ubah password"""
        try:
            # Load dengan password lama
            db = self._load_database(args.file, args.old_password)
            # Save dengan password baru
            db.save(args.new_password)
            
            print("✅ Password berhasil diubah")
            
        except Exception as e:
            print(f"❌ Error mengubah password: {e}")
            sys.exit(1)
    
    def handle_backup(self, args):
        """Handle perintah backup"""
        db = self._load_database(args.file, args.password)
        
        try:
            backup_password = args.backup_password or args.password
            db.backup(args.backup_file, backup_password)
            
            print(f"✅ Backup berhasil dibuat: {args.backup_file}")
            
        except Exception as e:
            print(f"❌ Error membuat backup: {e}")
            sys.exit(1)
    
    def run(self):
        """Jalankan CLI"""
        args = self.parser.parse_args()
        
        if not args.command:
            self.parser.print_help()
            return
        
        # Route commands to appropriate handlers
        command_handlers = {
            'create': {
                'database': self.handle_create_database,
                'table': self.handle_create_table
            },
            'insert': self.handle_insert,
            'select': self.handle_select,
            'update': self.handle_update,
            'delete': self.handle_delete,
            'info': self.handle_info,
            'password': self.handle_password,
            'backup': self.handle_backup
        }
        
        try:
            if args.command == 'create':
                handler = command_handlers['create'][args.create_command]
            else:
                handler = command_handlers[args.command]
            
            handler(args)
            
        except KeyError:
            print(f"❌ Perintah tidak valid: {args.command}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)


def main():
    """Fungsi utama"""
    cli = PyDBCLI()
    cli.run()


if __name__ == "__main__":
    main()