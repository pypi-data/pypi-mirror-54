import json
import os
import pytest

from jelm.core.jelm_class import Jelm
from jelm.core.io import reads_json, read_json


def test_json_reads():

    test_dic = {
        'metadata': {'author': 'me'},
        'objects': []
    }

    dump = json.dumps(test_dic)

    el = reads_json(dump)

    assert isinstance(el, Jelm)


def test_json_read(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "fing.jelm"

    test_dic = {
        'metadata': {'author': 'me'},
        'objects': []
    }

    dump = json.dumps(test_dic)

    p.write_text(dump)

    fp = os.fspath(p)

    el = read_json(fp)

    assert isinstance(el, Jelm)


def test_json_dump(tmp_path):
    d = tmp_path / "sub2"
    d.mkdir()
    p = d / "fing1.jelm"
    p2 = d / "fing2.jelm"

    test_dic = {
        'metadata': {'author': 'me'},
        'objects': [{'type': 'node',
                     'id': 'n1'}]
    }

    el = Jelm(**test_dic)

    assert isinstance(el.dict(), dict)

    assert el.dict() == test_dic

    assert isinstance(el.json_dumps(),
                      str)

    fp = os.fspath(p)
    fp2 = os.fspath(p2)

    el.json_dump(fp)
    el.json_dump(open(fp2,
                      'w'))

    el2 = read_json(fp)
    el3 = read_json(fp2)

    assert el.dict() == el2.dict()
    assert el.dict() == el3.dict()

    with pytest.raises(TypeError):
        el.json_dump(10)
