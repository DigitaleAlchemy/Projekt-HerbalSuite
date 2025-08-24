
from typing import Callable, Dict
from PySide6 import QtWidgets

_creators: Dict[str, Callable[[], QtWidgets.QWidget]] = {}

def register(key: str):
    def deco(func: Callable[[], QtWidgets.QWidget]):
        _creators[key] = func
        return func
    return deco

def create_page(key: str):
    maker = _creators.get(key)
    return maker() if maker else None

# Import builtin example plugins
from . import start, patients
