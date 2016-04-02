import os
import io
import pytest

import libconf


CURDIR = os.path.abspath(os.path.dirname(__file__))

def test_example_config():
    example_file = os.path.join(CURDIR, 'test_e2e.cfg') 
    with io.open(example_file, 'r', encoding='utf-8') as f:
        c = libconf.load(f, includedir=CURDIR)

    assert c.appconfig.version == 37
    assert c.appconfig['version-long'] == 370000000000000
    assert c.appconfig['version-autolong'] == 370000000000000
    assert c.appconfig.name == "libconf"
    assert c.appconfig.delimiter == False
    assert c.appconfig.works == True
    assert c.appconfig.allows == 0xA
    assert c.appconfig['eol-comments'] == 0xA
    assert c.appconfig.list == (3, "chicken", (), dict(group=True))
    assert c.appconfig.sub_group.sub_sub_group.yes == "yes"
    assert c.appconfig.sub_group.sub_sub_group['include-works'] == True
    assert c.appconfig.sub_group.arr == [1, "2", True]
    assert c.appconfig.sub_group.str == "Strings are joined despite comments";

def test_string_merging():
    # Unicode characters are supported, \u escapes not.
    input = u"""s = "abc\x21def\n" /* comment */ "newline-" # second comment
                   "here \u2603 \\u2603";"""
    assert libconf.loads(input).s == u"abc\x21def\nnewline-here \u2603 \\u2603"

def test_nonexisting_include_raises():
    input = u'''@include "/NON_EXISTING_FILE/DOESNT_EXIST"'''
    with pytest.raises(libconf.ConfigParseError):
        libconf.loads(input)

def test_circular_include_raises():
    circular_file = os.path.join(CURDIR, 'circular1.cfg') 
    with io.open(circular_file, 'r', encoding='utf-8') as f:
        with pytest.raises(libconf.ConfigParseError):
            libconf.load(f, includedir=CURDIR)
