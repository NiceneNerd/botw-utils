""" Functions to estimate RSTB values for complex file types """
import math
import sys
from pathlib import Path
from typing import Union, Optional

from oead import yaz0


class BfresSizeGuesser:
    multiplier_map = {
        True: {  # Big-Endian
            True: {  # Tex
                range(0, 100): 9.0,
                range(100, 2_000): 7.0,
                range(2_000, 3_000): 5.0,
                range(3_000, 4_000): 4.0,
                range(4_000, 8_500): 3.0,
                range(8_500, 12_000): 2.0,
                range(12_000, 17_000): 1.75,
                range(17_000, 30_000): 1.5,
                range(30_000, 45_000): 1.3,
                range(45_000, 100_000): 1.2,
                range(100_000, 150_000): 1.1,
                range(150_000, 200_000): 1.07,
                range(200_000, 250_000): 1.045,
                range(250_000, 300_000): 1.035,
                range(300_000, 600_000): 1.03,
                range(600_000, 1_000_000): 1.015,
                range(1_000_000, 1_800_000): 1.009,
                range(1_800_000, 4_500_000): 1.005,
                range(4_500_000, 6_000_000): 1.002,
                range(6_000_000, sys.maxsize): 1.0015,
            },
            False: {  # Model
                range(0, 500): 7.0,
                range(500, 750): 5.0,
                range(750, 1_250): 4.0,
                range(1_250, 2_000): 3.5,
                range(2_000, 400_000): 2.25,
                range(400_000, 600_000): 2.1,
                range(600_000, 1_000_000): 1.95,
                range(1_000_000, 1_500_000): 1.85,
                range(1_500_000, 3_000_000): 1.66,
                range(3_000_000, sys.maxsize): 1.45
            },
        },
        False: {  # Little-Endian
            True: {  # Tex
                range(0, 10_000): 2.0,
                range(10_000, 30_000): 1.5,
                range(30_000, 50_000): 1.3,
                range(50_000, sys.maxsize): 1.2,
            },
            False: {  # Model
                range(0, 1_250): 9.5,
                range(1_250, 2_500): 6.0,
                range(2_500, 50_000): 4.25,
                range(50_000, 100_000): 3.66,
                range(100_000, 800_000): 3.5,
                range(800_000, 2_000_000): 3.15,
                range(2_000_000, 3_000_000): 2.5,
                range(3_000_000, 4_000_000): 1.667,
                range(4_000_000, sys.maxsize): 1.5
            },
        },
    }

    @classmethod
    def guess(cls, be: bool, tex: bool, size: int):
        size *= 1.05

        for k, v in cls.multiplier_map[be][tex].items():
            if size in k:
                return size * v


class AampSizeGuesser:
    multiplier_map = {
        '.baiprog': {
            range(0, 380): 7.0,
            range(380, 400): 6.0,
            range(400, 450): 5.5,
            range(450, 600): 5.0,
            range(600, 1_000): 4.0,
            range(1_000, 1_750): 3.5,
            range(1_750, sys.maxsize): 3.0,
        },
        '.bas': {
            range(0, 100): 20.0,
            range(100, 200): 12.5,
            range(200, 300): 10.0,
            range(300, 600): 8.0,
            range(600, 1_500): 6.0,
            range(1_500, 2_000): 5.5,
            range(2_000, 15_000): 5.0,
            range(15_000, sys.maxsize): 4.5,
        },
        '.baslist': {
            range(0, 100): 15.0,
            range(100, 200): 10.0,
            range(200, 300): 8.0,
            range(300, 500): 6.0,
            range(500, 800): 5.0,
            range(800, 4_000): 4.0,
            range(4_000, sys.maxsize): 3.5,
        },
        '.bdrop': {
            range(0, 200): 8.5,
            range(200, 250): 7.0,
            range(250, 350): 6.0,
            range(350, 450): 5.25,
            range(450, 850): 4.5,
            range(850, sys.maxsize): 4.0
        },
        '.bgparamlist': {
            range(0, 100): 20.0,
            range(100, 150): 12.0,
            range(150, 250): 10.0,
            range(250, 350): 8.0,
            range(350, 450): 7.0,
            range(450, sys.maxsize): 6.0
        },
        '.brecipe': {
            range(0, 100): 12.5,
            range(100, 160): 8.5,
            range(160, 200): 7.5,
            range(200, 215): 7.0,
            range(215, sys.maxsize): 6.5,
        },
        '.bshop': {
            range(0, 200): 7.25,
            range(200, 400): 6.0,
            range(400, 500): 5.0,
            range(500, sys.maxsize): 4.05
        },
        '.bxml': {
            range(0, 350): 6.0,
            range(350, 450): 5.0,
            range(450, 550): 4.5,
            range(550, 650): 4.0,
            range(650, 800): 3.5,
            range(800, sys.maxsize): 3.0
        }
    }

    @classmethod
    def guess(cls, be: bool, ext: str, size: int):
        size *= 1.05

        if ext == '.bas':
            size *= 1.05  # I guess?

        if ext in cls.multiplier_map:
            for k, v in cls.multiplier_map[ext].items():
                if size in k:
                    ret = size * v
                    break
            else:
                raise NotImplementedError("Cannot happen ever lol")

        elif ext == '.bdmgparam':
            ret = (((-0.0018 * size) + 6.6273) * size) + 500
        elif ext == '.bphysics':
            ret = (((int(size) + 32) & -32) + 0x4E + 0x324) * max(4 * math.floor(size / 1388), 3)
        else:
            ret = 0

        return int(ret * 1.5 if not be else ret)


def guess_bfres_size(file: Union[Path, bytes], be: bool, name: Optional[str]) -> int:
    """Attempts to estimate a valid RSTB value for a BFRES file. Decompresses first if yaz0 encoded.

    Args:
        file (Union[Path, bytes]): The file to analyze, either as a Path or bytes.
        be (bool): Big-Endian (True) or Little-Endian (False)
        name (Optional[str]): The name of the BFRES file, used to detect type when there is no path.

    Raises:
        ValueError: Raises error if BFRES name is blank when passing file as bytes

    Returns:
        int: Return an estimated RSTB value
    """
    if isinstance(file, bytes):
        real_size = yaz0.get_header(file[0:16]).uncompressed_size if file[:4] == b"Yaz0" else len(file)
    elif isinstance(file, Path):
        name = file.name if not name else name
        with file.open('rb') as f:
            chunk = f.read(16)
            real_size = yaz0.get_header(chunk).uncompressed_size if chunk[:4] == b"Yaz0" else file.stat().st_size
    else:
        raise NotImplementedError()

    if not name:
        raise ValueError('BFRES name must not be blank if passing file as bytes.')

    return int(BfresSizeGuesser.guess(be, ".Tex" in name, real_size))


def guess_aamp_size(file: Union[Path, bytes], be: bool, ext: Optional[str]) -> int:
    """Attempts to estimate a valid RSTB value for an AAMP file. Decompresses first if yaz0 encoded.

    Args:
        file (Union[Path, bytes]): The file to analyze, either as a Path or bytes.
        be (bool): Big-Endian (True) or Little-Endian (False)
        ext (Optional[str]): The extension of the AAMP file, used to detect type when there is no path.

    Raises:
        ValueError: Raises error if extension is blank when passing file as bytes

    Returns:
        int: Returns an estimated RSTB value, or 0 for unsupported AAMP types.
    """
    if isinstance(file, bytes):
        real_size = yaz0.get_header(file[0:16]).uncompressed_size if file[:4] == b"Yaz0" else len(file)
    elif isinstance(file, Path):
        ext = file.name if not ext else ext
        with file.open('rb') as f:
            chunk = f.read(16)
            real_size = yaz0.get_header(chunk).uncompressed_size if chunk[:4] == b"Yaz0" else file.stat().st_size
    else:
        raise NotImplementedError()

    if not ext:
        raise ValueError('AAMP extension must not be blank if passing file as bytes.')

    return int(AampSizeGuesser.guess(be, ext, real_size))
