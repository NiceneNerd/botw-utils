from botw import get_canon_name, hashes, rstb


def test_canon():
    assert (
        get_canon_name("content\\Actor\\Pack\\Enemy_Lizal_Senior.sbactorpack")
        == "Actor/Pack/Enemy_Lizal_Senior.bactorpack"
    )
    assert (
        get_canon_name("aoc/0010/Map/MainField/A-1/A-1_Dynamic.smubin")
        == "Aoc/0010/Map/MainField/A-1/A-1_Dynamic.mubin"
    )
    assert (
        get_canon_name(
            "atmosphere/contents/01007EF00011E000/romfs/Actor/ActorInfo.product.sbyml"
        )
        == "Actor/ActorInfo.product.byml"
    )
    assert (
        get_canon_name(
            "atmosphere/contents/01007EF00011F001/romfs/Pack/AocMainField.pack"
        )
        == "Aoc/0010/Pack/AocMainField.pack"
    )
    try:
        get_canon_name("Hello/sweetie")
    except ValueError:
        pass
    else:
        raise AssertionError("Hello/sweetie allowed as canon path")
    assert (
        get_canon_name("Event/EventInfo.product.sbyml", no_root=True)
        == "Event/EventInfo.product.byml"
    )


def test_hashes():
    # pylint: disable=protected-access
    table_u = hashes.StockHashTable(True)
    table_nx = hashes.StockHashTable(False)
    assert table_u._table.get("Actor/ModelList/DgnMrgPrt_Dungeon023.bmodellist") == {
        2304172004,
        1028910535,
    }
    assert table_nx._table.get("Actor/ActorInfo.product.byml") == {3409334108}
    assert table_u.is_file_modded(
        "Actor/Physics/FldObj_MountainSheikerWall_A_06.bphysics", b""
    )
    assert not table_nx.is_file_modded("System/Version.txt", b"1.6.0")
    assert len(table_u.list_stock_files()) == 115895
    assert len(table_nx.list_stock_files()) == 119140


def test_rstb():
    buf = bytearray(388352)
    assert rstb.guess_bfres_size(memoryview(buf), True, "Link.sbfres") >= 498776
    buf = bytearray(1609904)
    assert rstb.guess_bfres_size(memoryview(buf), False, "Link.Tex.sbfres") >= 1619112
    buf = bytearray(436)
    assert rstb.guess_aamp_size(memoryview(buf), True, ".bxml") >= 1940
    assert rstb.guess_aamp_size(memoryview(buf), False, ".bxml") >= 2792
