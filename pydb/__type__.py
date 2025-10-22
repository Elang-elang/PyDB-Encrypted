class Number:
    """Class Number yang menggabungkan semua fitur int dan float"""
    
    def __init__(self, value):
        # Tentukan tipe dan konversi
        if isinstance(value, int):
            self._value = value
            self._type = int
        elif isinstance(value, float):
            self._value = value
            self._type = float
        else:
            # Coba konversi
            try:
                self._value = int(value)
                self._type = int
            except (ValueError, TypeError):
                try:
                    self._value = float(value)
                    self._type = float
                except (ValueError, TypeError):
                    raise TypeError(f"Cannot convert {value} to int or float")
    
    # ===== PROPERTIES =====
    @property
    def value(self):
        return self._value
    
    @property
    def type(self):
        return self._type
    
    @property
    def real(self):
        return self._value
    
    @property
    def imag(self):
        return 0
    
    @property
    def numerator(self):
        if self._type == int:
            return abs(self._value)
        else:
            return self.as_integer_ratio()[0]
    
    @property
    def denominator(self):
        if self._type == int:
            return 1
        else:
            return self.as_integer_ratio()[1]
    
    # ===== METHOD INTEGER =====
    def bit_length(self):
        return self._get_int_value().bit_length()
    
    def bit_count(self):
        return self._get_int_value().bit_count()
    
    def to_bytes(self, length, byteorder='big', signed=False):
        return self._get_int_value().to_bytes(length, byteorder, signed=signed)
    
    @classmethod
    def from_bytes(cls, bytes, byteorder='big', signed=False):
        return cls(int.from_bytes(bytes, byteorder, signed=signed))
    
    def conjugate(self):
        return Number(self._value)
    
    # ===== METHOD FLOAT =====
    def as_integer_ratio(self):
        if self._type == int:
            return (self._value, 1)
        else:
            return self._value.as_integer_ratio()
    
    def is_integer(self):
        if self._type == int:
            return True
        else:
            return self._value.is_integer()
    
    def hex(self):
        if self._type == int:
            return hex(self._value)
        else:
            return float.hex(self._value)
    
    @classmethod
    def fromhex(cls, string):
        if 'p' in string.lower() or '.' in string:
            return cls(float.fromhex(string))
        else:
            hex_str = string[2:] if string.startswith('0x') else string
            return cls(int(hex_str, 16))
    
    # ===== KONVERSI =====
    def _get_int_value(self):
        if self._type == int:
            return self._value
        else:
            return int(self._value)
    
    def to_int(self):
        return int(self._value)
    
    def to_float(self):
        return float(self._value)
    
    def __int__(self):
        return self.to_int()
    
    def __float__(self):
        return self.to_float()
    
    def __complex__(self):
        return complex(self._value)
    
    def __bool__(self):
        return bool(self._value)
    
    def __index__(self):
        return self._get_int_value()
    
    # ===== OPERATOR MATEMATIKA =====
    def _get_other_value(self, other):
        if isinstance(other, Number):
            return other._value
        return other
    
    def __add__(self, other):
        return Number(self._value + self._get_other_value(other))
    
    def __sub__(self, other):
        return Number(self._value - self._get_other_value(other))
    
    def __mul__(self, other):
        return Number(self._value * self._get_other_value(other))
    
    def __truediv__(self, other):
        return Number(self._value / self._get_other_value(other))
    
    def __floordiv__(self, other):
        return Number(self._value // self._get_other_value(other))
    
    def __mod__(self, other):
        return Number(self._value % self._get_other_value(other))
    
    def __divmod__(self, other):
        quotient, remainder = divmod(self._value, self._get_other_value(other))
        return (Number(quotient), Number(remainder))
    
    def __pow__(self, other, mod=None):
        if mod is not None:
            return Number(pow(self._value, self._get_other_value(other), self._get_other_value(mod)))
        return Number(self._value ** self._get_other_value(other))
    
    # Reverse operators
    def __radd__(self, other):
        return Number(other + self._value)
    
    def __rsub__(self, other):
        return Number(other - self._value)
    
    def __rmul__(self, other):
        return Number(other * self._value)
    
    def __rtruediv__(self, other):
        return Number(other / self._value)
    
    def __rfloordiv__(self, other):
        return Number(other // self._value)
    
    def __rmod__(self, other):
        return Number(other % self._value)
    
    def __rdivmod__(self, other):
        quotient, remainder = divmod(other, self._value)
        return (Number(quotient), Number(remainder))
    
    def __rpow__(self, other):
        return Number(other ** self._value)
    
    # ===== OPERATOR BITWISE =====
    def __and__(self, other):
        return Number(self._get_int_value() & int(self._get_other_value(other)))
    
    def __or__(self, other):
        return Number(self._get_int_value() | int(self._get_other_value(other)))
    
    def __xor__(self, other):
        return Number(self._get_int_value() ^ int(self._get_other_value(other)))
    
    def __lshift__(self, other):
        return Number(self._get_int_value() << int(self._get_other_value(other)))
    
    def __rshift__(self, other):
        return Number(self._get_int_value() >> int(self._get_other_value(other)))
    
    def __invert__(self):
        return Number(~self._get_int_value())
    
    # Reverse bitwise operators
    def __rand__(self, other):
        return Number(int(other) & self._get_int_value())
    
    def __ror__(self, other):
        return Number(int(other) | self._get_int_value())
    
    def __rxor__(self, other):
        return Number(int(other) ^ self._get_int_value())
    
    def __rlshift__(self, other):
        return Number(int(other) << self._get_int_value())
    
    def __rrshift__(self, other):
        return Number(int(other) >> self._get_int_value())
    
    # ===== OPERATOR PERBANDINGAN =====
    def __eq__(self, other):
        return self._value == self._get_other_value(other)
    
    def __ne__(self, other):
        return self._value != self._get_other_value(other)
    
    def __lt__(self, other):
        return self._value < self._get_other_value(other)
    
    def __le__(self, other):
        return self._value <= self._get_other_value(other)
    
    def __gt__(self, other):
        return self._value > self._get_other_value(other)
    
    def __ge__(self, other):
        return self._value >= self._get_other_value(other)
    
    # ===== REPRESENTASI =====
    def __repr__(self):
        return f"Number({self._value})"
    
    def __str__(self):
        return str(self._value)
    
    def __format__(self, format_spec):
        return format(self._value, format_spec)
    
    def __hash__(self):
        return hash(self._value)
    
    # ===== CUSTOM ISINSTANCE CHECK =====
    def is_integer_type(self):
        """Check jika Number berisi integer"""
        return self._type == int
    
    def is_float_type(self):
        """Check jika Number berisi float"""
        return self._type == float

# Fungsi helper untuk check isinstance
def is_number_instance(obj, types):
    """Custom isinstance check untuk Number"""
    if not isinstance(obj, Number):
        return False
    
    if types == int or types == float:
        return obj.type == types
    elif isinstance(types, tuple):
        return any(obj.type == t for t in types if t in (int, float))
    
    return False

class Boolean:
    """Class Boolean yang mengemas nilai bool dengan method tambahan"""
    
    def __init__(self, value=False):
        # Convert berbagai tipe ke bool
        if isinstance(value, Boolean):
            self._value = value._value
        elif isinstance(value, bool):
            self._value = value
        elif isinstance(value, (int, float)):
            self._value = bool(value)
        elif isinstance(value, str):
            self._value = value.lower() in ['true', '1', 'yes', 'on', 'y']
        else:
            self._value = bool(value)
    
    @property
    def value(self):
        """Mendapatkan nilai bool asli"""
        return self._value
    
    # Method untuk representasi
    def __repr__(self):
        return f"Boolean({self._value})"
    
    def __str__(self):
        return str(self._value)
    
    # Method untuk boolean context
    def __bool__(self):
        return self._value
    
    # Method untuk comparison
    def __eq__(self, other):
        if isinstance(other, Boolean):
            return self._value == other._value
        elif isinstance(other, bool):
            return self._value == other
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    # Method untuk hashing
    def __hash__(self):
        return hash(self._value)
    
    # Method Boolean-specific
    def negate(self):
        """Membalik nilai boolean"""
        return Boolean(not self._value)
    
    def and_op(self, other):
        """Operasi AND dengan nilai lain"""
        if isinstance(other, Boolean):
            return Boolean(self._value and other._value)
        return Boolean(self._value and bool(other))
    
    def or_op(self, other):
        """Operasi OR dengan nilai lain"""
        if isinstance(other, Boolean):
            return Boolean(self._value or other._value)
        return Boolean(self._value or bool(other))
    
    def xor_op(self, other):
        """Operasi XOR dengan nilai lain"""
        if isinstance(other, Boolean):
            return Boolean(self._value != other._value)
        return Boolean(self._value != bool(other))
    
    def implies(self, other):
        """Operasi implication (jika-maka)"""
        if isinstance(other, Boolean):
            return Boolean(not self._value or other._value)
        return Boolean(not self._value or bool(other))
    
    def to_string(self):
        """Mengkonversi ke String"""
        from string_type import String
        return String("True" if self._value else "False")
    
    def to_integer(self):
        """Mengkonversi ke Integer (True=1, False=0)"""
        from integer_type import Integer
        return Integer(1 if self._value else 0)
    
    def to_float(self):
        """Mengkonversi ke Float (True=1.0, False=0.0)"""
        from float_type import Float
        return Float(1.0 if self._value else 0.0)
    
    def to_yes_no(self):
        """Mengembalikan 'Yes' atau 'No'"""
        from string_type import String
        return String("Yes" if self._value else "No")
    
    def to_on_off(self):
        """Mengembalikan 'On' atau 'Off'"""
        from string_type import String
        return String("On" if self._value else "Off")
    
    def to_1_0(self):
        """Mengembalikan '1' atau '0'"""
        from string_type import String
        return String("1" if self._value else "0")
    
    def is_true(self):
        """Cek jika nilai True"""
        return self._value
    
    def is_false(self):
        """Cek jika nilai False"""
        return not self._value
    
    # Static methods dan class methods
    @classmethod
    def true(cls):
        """Membuat Boolean True"""
        return cls(True)
    
    @classmethod
    def false(cls):
        """Membuat Boolean False"""
        return cls(False)
    
    @staticmethod
    def parse(value):
        """Parse berbagai tipe ke Boolean"""
        return Boolean(value)
    
    # Method untuk identity checking
    def is_boolean(self):
        """Selalu return True karena ini adalah Boolean"""
        return True
    
    @classmethod
    def is_boolean_instance(cls, obj):
        """Check jika obj adalah instance Boolean"""
        return isinstance(obj, cls)

# String (masih bisa inherit dari str)
class String(str):
    def __init__(self, value=''):
        super().__init__()
    
    def to_upper(self):
        return String(self.upper())
    
    def to_lower(self):
        return String(self.lower())
    
    def to_boolean(self):
        true_values = ['true', '1', 'yes', 'on', 'y']
        false_values = ['false', '0', 'no', 'off', 'n']
        
        lower_str = self.lower().strip()
        if lower_str in true_values:
            return Boolean(True)
        elif lower_str in false_values:
            return Boolean(False)
        else:
            raise ValueError(f"Cannot convert '{self}' to Boolean")
    
    def is_string(self):
        return True

# Integer (masih bisa inherit dari int)
class Integer(int):
    def __init__(self, value=0):
        super().__init__()
    
    def to_boolean(self):
        return Boolean(bool(self))
    
    def is_even(self):
        return self % 2 == 0
    
    def is_integer(self):
        return True

# Float (masih bisa inherit dari float)
class Float(float):
    def __init__(self, value=0.0):
        super().__init__()
    
    def to_boolean(self):
        return Boolean(bool(self))
    
    def is_float(self):
        return True

# Null (menggunakan singleton pattern)
class Null:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
    
    def __repr__(self):
        return "Null()"
    
    def __str__(self):
        return "Null"
    
    def __bool__(self):
        return False
    
    def __eq__(self, other):
        return isinstance(other, Null) or other is None
    
    def to_boolean(self):
        return Boolean(False)
    
    def is_null(self):
        return True