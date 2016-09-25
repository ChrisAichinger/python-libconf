import os
import io
import pytest

import libconf

CURDIR = os.path.abspath(os.path.dirname(__file__))

def test_save_collection():
    c = [1, 2, 3]
    c_saved = libconf.save_collection(c)
    assert c_saved == '1,\n2,\n3'
    c = (1, 2, 3)
    c_saved = libconf.save_collection(c)
    assert c_saved == '1,\n2,\n3'
    c = (( 1, 2), (3))
    c_saved = libconf.save_collection(c)
    assert c_saved == '(\n    1,\n    2\n),\n3'
    c = ([ 1, 2], (3))
    c_saved = libconf.save_collection(c)
    assert c_saved == '[\n    1,\n    2\n],\n3'
    c = [[ 1, 2], (3)]
    c_saved = libconf.save_collection(c)
    assert c_saved == '[\n    1,\n    2\n],\n3'

def test_saves():
    example_file = os.path.join(CURDIR, 'test_e2e.cfg')
    with io.open(example_file, 'r', encoding='utf-8') as f:
        c = libconf.load(f, includedir=CURDIR)
    c_saved = libconf.loads(libconf.saves(c))
    assert c == c_saved

def test_save():
    example_file = os.path.join(CURDIR, 'test_e2e.cfg')
    with io.open(example_file, 'r', encoding='utf-8') as f:
        c = libconf.load(f, includedir=CURDIR)
    with open('test_e2e_copy.cfg', 'w+') as f:
        libconf.save(c, f)
    with io.open('test_e2e_copy.cfg', 'r', encoding='utf-8') as f:
        c_saved = libconf.load(f, includedir=CURDIR)
    assert c == c_saved
