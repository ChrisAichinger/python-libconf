import os
import io
import pytest

import libconf

CURDIR = os.path.abspath(os.path.dirname(__file__))

def test_dump_collection():
    c = [1, 2, 3]
    c_dumpd = libconf.dump_collection(c)
    assert c_dumpd == '1,\n2,\n3'
    c = (1, 2, 3)
    c_dumpd = libconf.dump_collection(c)
    assert c_dumpd == '1,\n2,\n3'
    c = (( 1, 2), (3))
    c_dumpd = libconf.dump_collection(c)
    assert c_dumpd == '(\n    1,\n    2\n),\n3'
    c = ([ 1, 2], (3))
    c_dumpd = libconf.dump_collection(c)
    assert c_dumpd == '[\n    1,\n    2\n],\n3'
    c = [[ 1, 2], (3)]
    c_dumpd = libconf.dump_collection(c)
    assert c_dumpd == '[\n    1,\n    2\n],\n3'

def test_dump_string():
    c = { 'name' : 'name'}
    c_dumpd = libconf.dump_dict(c)
    assert c_dumpd == 'name = "name"'

    c = { 'name' : 'x\01\""name"\"\\'}
    c_dumpd = libconf.dump_dict(c)
    assert c_dumpd == 'name = "x\01\""name"\"\\"'

def test_config_int_to_str():
    assert libconf.config_int_to_str(0) == '0'
    assert libconf.config_int_to_str(pow(2, 31) - 1) == str(pow(2, 31) - 1);
    assert libconf.config_int_to_str(pow(2, 31)) == str(pow(2, 31)) + 'L';
    assert libconf.config_int_to_str(-pow(2, 31)) == str(-pow(2, 31));
    assert libconf.config_int_to_str(-pow(2, 31) - 1) == str(-pow(2, 31) - 1) + 'L';

def test_dumps():
    example_file = os.path.join(CURDIR, 'test_e2e.cfg')
    with io.open(example_file, 'r', encoding='utf-8') as f:
        c = libconf.load(f, includedir=CURDIR)
    c_dumpd = libconf.loads(libconf.dumps(c))
    assert c == c_dumpd

def test_dump():
    example_file = os.path.join(CURDIR, 'test_e2e.cfg')
    with io.open(example_file, 'r', encoding='utf-8') as f:
        c = libconf.load(f, includedir=CURDIR)
    with open('test_e2e_copy.cfg', 'w+') as f:
        libconf.dump(c, f)
    with io.open('test_e2e_copy.cfg', 'r', encoding='utf-8') as f:
        c_dumpd = libconf.load(f, includedir=CURDIR)
    assert c == c_dumpd
