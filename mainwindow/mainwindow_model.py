from typing import List, Optional
from casacore.tables import table as Table

from PySide6.QtCore import QAbstractTableModel

class MainWindowModel:
    """doc"""
    #tables: List[str] = [] # this is stored by listviewmodel
    selected_table: Optional[Table] = None
    taqlquery: str = ""
    #last_table_query: Optional[str] = None
