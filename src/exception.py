from typing import List, Any

class Error(SyntaxError, Exception):
    def __init__(self, ErrorText: str):
        self.ErrorText = ErrorText; super().__init__(ErrorText)
        
    def __repr__(self):
        return f"Error({self.ErrorText})"


class IsConstantError(Error, ValueError):
    def __init__(self, ErrorText: str):
        self.ErrorText = ErrorText; super().__init__(ErrorText)
        
    def __repr__(self):
        return f"IsConstantError({self.ErrorText})"


class RedeclareError(Error, ValueError):
    def __init__(self, ErrorText: str):
        self.ErrorText = ErrorText; super().__init__(ErrorText)
        
    def __repr__(self):
        return f"RedeclareError({self.ErrorText})"


class NotModifierError(Error):
    def __init__(self, ErrorText: str):
        self.ErrorText = ErrorText; super().__init__(ErrorText)
        
    def __repr__(self):
        return f"NotModifierError({self.ErrorText})"


class UndefineError(Error, ValueError):
    def __init__(self, ErrorText: str):
        self.ErrorText = ErrorText; super().__init__(ErrorText)
        
    def __repr__(self):
        return f"UndefineError({self.ErrorText})"


class EventError(Error):
    def __init__(self, ErrorText: str):
        self.ErrorText = ErrorText; super().__init__(ErrorText)
        
    def __repr__(self):
        return f"EventError({self.ErrorText})"


class CloseEventError(EventError):
    def __init__(self, ErrorText: str):
        self.ErrorText = ErrorText; super().__init__(ErrorText)
        
    def __repr__(self):
        return f"CloseEventError({self.ErrorText})"


class OpenEventError(EventError):
    def __init__(self, ErrorText: str):
        self.ErrorText = ErrorText; super().__init__(ErrorText)
        
    def __repr__(self):
        return f"OpenEventError({self.ErrorText})"


class StatementError(EventError):
    def __init__(self, ErrorText: str):
        self.ErrorText = ErrorText; super().__init__(ErrorText)
        
    def __repr__(self):
        return f"StatementError({self.ErrorText})"


class CompileError(EventError):
    def __init__(self, ErrorText: str):
        self.ErrorText = ErrorText; super().__init__(ErrorText)
        
    def __repr__(self):
        return f"CompileError({self.ErrorText})"
        
    def Template_ErrorList(self, *ErrorList: List[Any]):
        super().__init__(f"Eror karena bahasa tidak terdaftar. {{Bahasa yang tidak diketahui: {ErrorList[0]}}}, {{Bahasa yang terdaftar: ({ErrorList[1]})}}")


class AttributeArgsError(EventError, UndefineError, IndexError):
    def __init__(self, ErrorText: str):
        self.ErrorText = ErrorText; super().__init__(ErrorText)
        
    def __repr__(self):
        return f"AttributeArgsError({self.ErrorText})"


class TypeObjectError(Error, TypeError):
    def __init__(self, ErrorText: str):
        self.ErrorText = ErrorText; super().__init__(ErrorText)
        
    def __repr__(self):
        return f"TypeObjectError({self.ErrorText})"


class TypeArrayError(TypeObjectError):
    def __init__(self, ErrorText: str):
        self.ErrorText = ErrorText; super().__init__(ErrorText)
        
    def __repr__(self):
        return f"TypeArrayError({self.ErrorText})"


class TypeDictionaryError(TypeArrayError):
    def __init__(self, ErrorText: str):
        self.ErrorText = ErrorText; super().__init__(ErrorText)
        
    def __repr__(self):
        return f"TypeDictionaryError({self.ErrorText})"


class LanguageError(Error, TypeError):
    def __init__(self, ErrorText: str):
        self.ErrorText = ErrorText; super().__init__(ErrorText)
        
    def __repr__(self):
        return f"LanguageError({self.ErrorText})"


class DatabaseError(EventError):
    def __init__(self, ErrorText: str):
        self.ErrorText = ErrorText; super().__init__(ErrorText)
        
    def __repr__(self):
        return f"DatabaseError({self.ErrorText})"


class DatabaseLengthError(DatabaseError, IndexError):
    def __init__(self, ErrorText: str):
        self.ErrorText = ErrorText; super().__init__(ErrorText)
        
    def __repr__(self):
        return f"DatabaseLengtgError({self.ErrorText})"


class DatabaseColumnError(DatabaseError, IndexError):
    def __init__(self, ErrorText: str):
        self.ErrorText = ErrorText; super().__init__(ErrorText)
        
    def __repr__(self):
        return f"DatabaseColumnError({self.ErrorText})"


class DatabaseTypeError(DatabaseError, TypeError):
    def __init__(self, ErrorText: str):
        self.ErrorText = ErrorText; super().__init__(ErrorText)
        
    def __repr__(self):
        return f"DatabaseTypeError({self.ErrorText})"


class DatabaseTableError(DatabaseError, IndexError, TypeError):
    def __init__(self, ErrorText: str):
        self.ErrorText = ErrorText; super().__init__(ErrorText)
        
    def __repr__(self):
        return f"DatabaseTableError({self.ErrorText})"

