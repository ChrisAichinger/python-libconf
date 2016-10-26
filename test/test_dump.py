import io
import pytest

import libconf


# Helper functions
##################

def dump_value(key, value, **kwargs):
    str_file = io.StringIO()
    libconf.dump_value(key, value, str_file, **kwargs)
    return str_file.getvalue()

def dump_collection(c, **kwargs):
    str_file = io.StringIO()
    libconf.dump_collection(c, str_file, **kwargs)
    return str_file.getvalue()

def dump_dict(c, **kwargs):
    str_file = io.StringIO()
    libconf.dump_dict(c, str_file, **kwargs)
    return str_file.getvalue()


# Actual tests
##############

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
    c_dumped = dump_collection(c, indent=4)
    assert c_dumped == '    [\n        1,\n        2\n    ],\n    3'

def test_dump_dict_simple_string():
    c = {'name': 'value'}
    c_dumped = dump_dict(c)
    assert c_dumped == 'name = "value";\n'

def test_dump_dict_indentation_dicts():
    c = {'a': {'b': 3}}
    c_dumped = dump_dict(c)
    assert c_dumped == 'a =\n{\n    b = 3;\n};\n'

def test_dump_dict_indentation_dicts_with_extra_indent():
    c = {'a': {'b': 3}}
    c_dumped = dump_dict(c, indent=4)
    assert c_dumped == '    a =\n    {\n        b = 3;\n    };\n'

def test_dump_dict_indentation_dicts_within_lists():
    c = {'a': [{'b': 3}]}
    c_dumped = dump_dict(c)
    assert c_dumped == 'a =\n[\n    {\n        b = 3;\n    }\n];\n'

def test_dump_string_escapes_backslashes():
    s = r'abc \ def \ hij'
    c_dumped = libconf.dump_string(s)
    assert c_dumped == r'"abc \\ def \\ hij"'

def test_dump_string_escapes_doublequotes():
    s = r'abc "" def'
    c_dumped = libconf.dump_string(s)
    assert c_dumped == r'"abc \"\" def"'

def test_dump_string_escapes_common_escape_characters():
    s = '\f \n \r \t'
    c_dumped = libconf.dump_string(s)
    assert c_dumped == r'"\f \n \r \t"'

def test_dump_string_escapes_unprintable_characters():
    s = '\x00 \x1f \x7f'
    c_dumped = libconf.dump_string(s)
    assert c_dumped == r'"\x00 \x1f \x7f"'

def test_dump_string_keeps_8bit_chars_intact():
    s = '\x80 \x9d \xff'
    c_dumped = libconf.dump_string(s)
    assert c_dumped == '"\x80 \x9d \xff"'

def test_dump_string_handles_unicode_strings():
    s = u'\u2603'
    c_dumped = libconf.dump_string(s)
    assert c_dumped == u'"\u2603"'

def test_dump_boolean():
    c = (True, False)
    c_dumped = dump_collection(c)
    assert c_dumped == 'True,\nFalse'

def test_dump_int():
    assert libconf.dump_int(0) == '0'
    assert libconf.dump_int(-30) == '-30'
    assert libconf.dump_int(60) == '60'

def test_dump_int32_has_no_l_suffix():
    assert libconf.dump_int(2**31 - 1) == str(2**31 - 1)
    assert libconf.dump_int(-2**31) == str(-2**31)

def test_dump_int64_has_l_suffix():
    assert libconf.dump_int(2**31) == str(2**31) + 'L'
    assert libconf.dump_int(-2**31 - 1) == str(-2**31 - 1) + 'L'

def test_dump_raises_on_string_input():
    with pytest.raises(libconf.ConfigSerializeError):
        libconf.dumps("")

def test_dump_raises_on_list_input():
    with pytest.raises(libconf.ConfigSerializeError):
        libconf.dumps([])

def test_none_dict_key_raises():
    with pytest.raises(libconf.ConfigSerializeError):
        libconf.dumps({None: 0})

def test_integer_dict_key_raises():
    with pytest.raises(libconf.ConfigSerializeError):
        libconf.dumps({0: 0})

def test_invalid_value_raises():
    with pytest.raises(libconf.ConfigSerializeError):
        libconf.dumps({'a': object()})
