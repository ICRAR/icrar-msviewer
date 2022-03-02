from typing import List, Optional
from casacore.tables import table as Table
import numpy as np

class MainWindowModel:
    """doc"""
    #tables: List[str] = [] # this is stored by listviewmodel
    selected_table: Optional[Table] = None
    taqlquery: str = ""
    #last_table_query: Optional[str] = None


class TableModel:
    ms: Table
    msquery: Table
    query: str
    prev_query: str # used to determine when query is outdated
    dirty_image: np.ndarray


class MainWindowImprovedModel:
    """
    Model containing state per open measurement set
    """
    tables: List[TableModel]
    selected_table_index: int
