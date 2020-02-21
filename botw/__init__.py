import os
from pathlib import Path
from typing import Union

DATA_DIR = Path(os.path.dirname(os.path.realpath(__file__))) / 'data'

def get_canon_name(path: Union[str, Path], no_root: bool = False) -> str:
    r"""Gets the canonical resource path of a given BOTW file from its relative
    file system path.

    :param path: The file path to render canonical. This must be either a 
    relative path to a file in a mod or game folder, or it must be the stored
    path of a file inside a SARC. E.g. `content\Actor\ActorInfo.product.sbyml`
    is valid, but not `C:\botw_mods\content\Actor\ActorInfo.product.sbyml`.
    :type path: Union[str, Path]
    :param no_root: Specifies whether to allow paths that do not begin with a
    recognized game folder. This is necessary for paths inside SARCs. Defaults
    to False.
    :type no_root: bool
    :returns: Returns the canonical resource path for given file, or raises a
    ValueError.
    :rtype: str
    """
    if isinstance(path, Path):
        path = str(path)
    name = (path.replace('\\', '/')
                .replace('Content', 'content')
                .replace('Aoc', 'aoc')
                .replace('atmosphere/titles/', '')
                .replace('atmosphere/contents/', '')
                .replace('01007EF00011E000/romfs', 'content')
                .replace('01007EF00011E001/romfs', 'aoc/0010')
                .replace('01007EF00011E002/romfs', 'aoc/0010')
                .replace('01007EF00011F001/romfs', 'aoc/0010')
                .replace('01007EF00011F002/romfs', 'aoc/0010')
                .replace('romfs', 'content')
                .replace('.s', '.'))
    if name.startswith('aoc/'):
        return (name.replace('aoc/content', 'Aoc')
                    .replace('aoc', 'Aoc'))
    elif name.startswith('content/') and '/aoc' not in name:
        return name.replace('content/', '')
    else:
        if no_root:
            return name
        else:
            raise ValueError(
                f'{name} does not appear to be a canonical BOTW path'
            )
