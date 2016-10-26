import os
import io
import textwrap
import pytest

import libconf


CURDIR = os.path.abspath(os.path.dirname(__file__))


# Tests for load() and loads()
##############################

def test_loads_maintains_dict_order():
    config = libconf.loads(u'''l: 1; i: 5; b: 3; c: 1; o: 9; n: 0; f: 7;''')
    assert ''.join(config.keys()) == 'libconf'

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

def test_loads_of_bytes_throws():
    with pytest.raises(TypeError) as excinfo:
        libconf.loads(b'')

    assert 'libconf.loads' in str(excinfo.value)

def test_load_of_BytesIO_throws():
    with pytest.raises(TypeError) as excinfo:
        libconf.load(io.BytesIO(b'a: "37";'))

    assert 'libconf.load' in str(excinfo.value)


# Tests for dump() and dumps()
##############################

def test_dump_special_characters():
    d = {'a': ({'b': [u"\x00 \n \x7f abc \xff \u2603"]},)}
    s = libconf.dumps(d)

    expected = textwrap.dedent(u'''\
        a =
        (
            {
                b =
                [
                    "\\x00 \\n \\x7f abc \xff \u2603"
                ];
            }
        );
        ''')
    assert s == expected


# Tests for dump-load round trips
#################################

def test_dumps_roundtrip():
    example_file = os.path.join(CURDIR, 'test_e2e.cfg')
    with io.open(example_file, 'r', encoding='utf-8') as f:
        c = libconf.load(f, includedir=CURDIR)

    c_dumped = libconf.loads(libconf.dumps(c))

    assert c == c_dumped

def test_dump_roundtrip():
    example_file = os.path.join(CURDIR, 'test_e2e.cfg')
    with io.open(example_file, 'r', encoding='utf-8') as f:
        c = libconf.load(f, includedir=CURDIR)

    with io.StringIO() as f:
        libconf.dump(c, f)
        f.seek(0)
        c_dumped = libconf.load(f, includedir=CURDIR)

    assert c == c_dumped

def test_dump_special_characters_roundtrip():
    d = {'a': ({'b': [u"\x00 \n \x7f abc \xff \u2603"]},)}
    d2 = libconf.loads(libconf.dumps(d))
    assert d == d2

def test_roundtrip_preserves_config_entry_order():
    config = libconf.loads(u'''l: 1; i: 5; b: 3; c: 1; o: 9; n: 0; f: 7;''')
    dumped = libconf.dumps(config)
    reloaded = libconf.loads(dumped)

    assert ''.join(reloaded.keys()) == 'libconf'
