""" Provides hash tables for unmodified game files using xxHash """
# pylint: disable=bad-continuation
from json import loads
from functools import lru_cache
from typing import ByteString, Dict, Iterator, List, Union
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
    return loads((DATA_DIR / "wiiu_hashes.json").read_text("utf-8"))


@lru_cache(None)
def get_switch_hash_table() -> Dict[str, List[int]]:
    """
    Gets a hash table for game files in the unmodified 1.5.0 Switch version of
    BOTW. It comes as a dict with canonical path names as keys and lists of int
    values. The list contains multiple possible hashes for files with no
    modified content, including dirty versions affected by automatic processing
    through libraries and tools.
    """
    return loads((DATA_DIR / "switch_hashes.json").read_text("utf-8"))


class StockHashTable:
    """ A class wrapping a hash table for stock BOTW files with a few
    convenience methods. """

    _table: Dict[str, List[int]]

    def __init__(self, wiiu: bool):
        table = get_wiiu_hash_table() if wiiu else get_switch_hash_table()
        self._table = {file: set(xhashes) for file, xhashes in table.items()}
        del table

    @lru_cache(None)
    def is_file_modded(
        self, file_name: str, data: Union[ByteString, int], flag_new: bool = True
    ) -> bool:
        """Checks a file to see if it has been modified. Automatically decompresses yaz0 data.

        Args:
            file_name (str): The canonical resource path of the file to check
            data (Union[ByteString, int]): Either the file data (as a byteslike object) or an xxh32
                hash as an int
            flag_new (bool, optional): Whether to flag new files (not in vanilla BOTW) as modified.
                Defaults to True.

        Returns:
            bool: Returns whether the file's hash matches a known version of the hash for the
                original version.
        """
        if file_name not in self._table:
            return flag_new
        else:
            if isinstance(data, int):
                return data not in self._table[file_name]
            if data[0:4] == b"Yaz0":
                data = decompress(data)
            return xxh32_intdigest(data) not in self._table[file_name]

    @lru_cache(None)
    def is_file_new(self, file_name: str) -> bool:
        """Checks if a file is present in the unmodded game.

        Args:
            file_name (str): The canonical resource path of the file to check

        Returns:
            bool: Returns True if the file is present in the stock hash table.
        """
        return file_name in self._table

    def get_stock_files(self) -> Iterator[str]:
        """Iterates the files in the stock hash table by their canonical resource paths.

        Yields:
            Iterator[str]: Iterator for stock files in hash table
        """
        for file in self._table:
            yield file

    def list_stock_files(self) -> List[str]:
        """Lists all of the files in the stock hash table by their canonical resource paths.

        Returns:
            List[str]: List of stock files in hash table
        """
        return list(self._table.keys())
