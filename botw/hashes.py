""" Provides hash tables for unmodified game files using xxHash """
from json import loads
from functools import lru_cache
from typing import ByteString, Dict, List, Union
from xxhash import xxh32_intdigest

from oead.yaz0 import decompress
from . import DATA_DIR

@lru_cache(None)
def get_wiiu_hash_table() -> Dict[str, List[int]]:
    """
    Gets a hash table for game files in the unmodified 1.5.0 Wii U version of
    BOTW. It comes as a dict with canonical path names as keys and lists of int
    values. The list contains multiple possible hashes for files with no
    modified content, including dirty versions affected by automatic processing
    through libraries and tools.
    """ 
    return loads((DATA_DIR / 'wiiu_hashes.json').read_text('utf-8'))

@lru_cache(None)
def get_switch_hash_table() -> Dict[str, List[int]]:
    """
    Gets a hash table for game files in the unmodified 1.5.0 Switch version of
    BOTW. It comes as a dict with canonical path names as keys and lists of int
    values. The list contains multiple possible hashes for files with no
    modified content, including dirty versions affected by automatic processing
    through libraries and tools.
    """ 
    return loads((DATA_DIR / 'switch_hashes.json').read_text('utf-8'))

class HashTable:
    _table: Dict[str, List[int]]

    def __init__(self, wiiu: bool):
        self._table = get_wiiu_hash_table() if wiiu else get_switch_hash_table()

    @lru_cache(None)
    def is_file_modded(
        self,
        file_name: str,
        data: Union[ByteString, int],
        flag_new: bool = True
    ) -> bool:
        if file_name not in self._table:
            return flag_new
        else:
            if isinstance(data, int):
                xhash = data
            else:
                if data[0:4] == b'Yaz0':
                    data = decompress(data)
                xhash = xxh32_intdigest(data)
            return xhash in self._table[file_name]

