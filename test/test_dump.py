import os
import io
import pytest

import libconf

CURDIR = os.path.abspath(os.path.dirname(__file__))

def dump_collection(c):
    str_file = io.StringIO()
    libconf.dump_collection(c, str_file)
    return str_file.getvalue()

def dump_dict(c):
    str_file = io.StringIO()
    libconf.dump_dict(c, str_file)
    return str_file.getvalue()

def test_dump_collection():
    c = [1, 2, 3]
    c_dumped = dump_collection(c)
    assert c_dumped == '1,\n2,\n3'
    c = (1, 2, 3)
    c_dumped = dump_collection(c)
    assert c_dumped == '1,\n2,\n3'
    c = ((1, 2), (3))
    c_dumped = dump_collection(c)
    assert c_dumped == '(\n    1,\n    2\n),\n3'
    c = ([1, 2], (3))
    c_dumped = dump_collection(c)
    assert c_dumped == '[\n    1,\n    2\n],\n3'
    c = [[1, 2], (3)]
    c_dumped = dump_collection(c)
    assert c_dumped == '[\n    1,\n    2\n],\n3'

def test_dump_string():
    c = {'name' : 'name'}
    c_dumped = dump_dict(c)
    assert c_dumped == 'name = "name"'

    c = { 'name' : 'x\01\""name"\"\\'}
    c_dumped = dump_dict(c)
    assert c_dumped == 'name = "x\01\""name"\"\\"'

def test_dump_boolean():
    c = (True, False)
    c_dumped = dump_collection(c)
    assert c_dumped == 'True,\nFalse'

def test_config_int_to_str():
    assert libconf.config_int_to_str(0) == '0'
    assert libconf.config_int_to_str(pow(2, 31) - 1) == str(pow(2, 31) - 1)
    assert libconf.config_int_to_str(pow(2, 31)) == str(pow(2, 31)) + 'L'
    assert libconf.config_int_to_str(-pow(2, 31)) == str(-pow(2, 31))
    assert libconf.config_int_to_str(-pow(2, 31) - 1) == str(-pow(2, 31) - 1) + 'L'

def test_dumps():
    example_file = os.path.join(CURDIR, 'test_e2e.cfg')
    with io.open(example_file, 'r', encoding='utf-8') as f:
        c = libconf.load(f, includedir=CURDIR)
    c_dumped = libconf.loads(libconf.dumps(c))
    assert c == c_dumped

def test_dump():
    example_file = os.path.join(CURDIR, 'test_e2e.cfg')
    with io.open(example_file, 'r', encoding='utf-8') as f:
        c = libconf.load(f, includedir=CURDIR)
    with open('test_e2e_copy.cfg', 'w+') as f:
        libconf.dump(c, f)
    with io.open('test_e2e_copy.cfg', 'r', encoding='utf-8') as f:
        c_dumped = libconf.load(f, includedir=CURDIR)
    assert c == c_dumped
