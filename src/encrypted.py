import os
import json
import base64
from typing import Union, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class PasswordValueError(SyntaxError, ValueError):
    def __init__(self, ErrorText):
        self.ErrorText = ErrorText
        super().__init__(ErrorText)
    def __repr__(self):
        return f"PasswordValueError({ErrorText})"

class TextEncryptor:
    """
    Kelas untuk mengenkripsi dan mendekripsi teks menggunakan password
    """
    
    def __init__(self, password: str, salt: Optional[bytes] = None):
        """
        Inisialisasi encryptor dengan password
        
        Args:
            password: Password untuk enkripsi/dekripsi
            salt: Salt untuk key derivation (opsional)
        """
        if not password:
            raise PasswordValueError("Password tidak boleh kosong")
        
        self.password = password.encode('utf-8')
        self.salt = salt or os.urandom(16)
        self.fernet = self._generate_fernet_key()
    
    def _generate_fernet_key(self) -> Fernet:
        """Generate Fernet key dari password"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password))
        return Fernet(key)
    
    def encrypt_text(self, text: str) -> bytes:
        """
        Enkripsi teks menjadi bytes yang aman
        
        Args:
            text: Teks yang akan dienkripsi
            
        Returns:
            Bytes terenkripsi
        """
        if not isinstance(text, str):
            raise TypeError("Input harus string")
        
        encrypted_data = self.fernet.encrypt(text.encode('utf-8'))
        
        # Gabungkan salt dengan data terenkripsi untuk penyimpanan
        return self.salt + encrypted_data
    
    def decrypt_text(self, encrypted_bytes: bytes) -> str:
        """
        Dekripsi bytes menjadi teks asli
        
        Args:
            encrypted_bytes: Bytes terenkripsi
            
        Returns:
            Teks asli yang didekripsi
            
        Raises:
            PasswordValueError: Jika password salah atau data korup
        """
        if len(encrypted_bytes) < 16:
            raise PasswordValueError("Data terenkripsi tidak valid")
        
        # Ekstrak salt dari data
        salt = encrypted_bytes[:16]
        encrypted_data = encrypted_bytes[16:]
        
        # Buat Fernet instance baru dengan salt yang diekstrak
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password))
        fernet = Fernet(key)
        
        # Dekripsi data
        try:
            decrypted_data = fernet.decrypt(encrypted_data)
            return decrypted_data.decode('utf-8')
        except Exception as e:
            raise PasswordValueError(f"Gagal mendekripsi: Password salah atau data korup - {e}")

# =============================================================================
# FUNGSI SEDERHANA (Standalone)
# =============================================================================

def encrypt(text: str, password: str) -> bytes:
    """
    Enkripsi string menjadi bytes dengan password
    
    Args:
        text: Teks yang akan dienkripsi
        password: Password untuk enkripsi
        
    Returns:
        Bytes terenkripsi
    """
    encryptor = TextEncryptor(password)
    return encryptor.encrypt_text(text)

def decrypt(encrypted_bytes: bytes, password: str) -> str:
    """
    Dekripsi bytes menjadi string dengan password
    
    Args:
        encrypted_bytes: Bytes terenkripsi
        password: Password untuk dekripsi
        
    Returns:
        Teks asli yang didekripsi
    """
    encryptor = TextEncryptor(password)  # Salt akan diekstrak dari bytes
    return encryptor.decrypt_text(encrypted_bytes)

def save(text: str, password: str, file_path: str) -> None:
    """
    Simpan teks terenkripsi ke file
    
    Args:
        text: Teks yang akan disimpan
        password: Password untuk enkripsi
        file_path: Path file tujuan
    """
    encrypted_bytes = encrypt(text, password)
    with open(os.path.abspath(file_path), 'wb') as f:
        f.write(encrypted_bytes)

def load(password: str, file_path: str) -> str:
    """
    Muat dan dekripsi teks dari file
    
    Args:
        password: Password untuk dekripsi
        file_path: Path file sumber
        
    Returns:
        Teks asli yang didekripsi
    """
    with open(file_path, 'rb') as f:
        encrypted_bytes = f.read()
    return decrypt(encrypted_bytes, password)