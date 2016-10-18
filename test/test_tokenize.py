import pytest

import libconf


def test_float():
    tokenizer = libconf.Tokenizer("<memory>")

    tokens = list(tokenizer.tokenize(" 2.  .5  0.75  1.0E1 "
                                     "+2. +.5 +0.75 +1.0E1 "
                                     "-2. -.5 -0.75 -1.0E1 "
                                     "2.E3 .5E6 0.75E9 1.0E1 "
                                     "2.E+3 .5E+6 0.75E+9 1.0E+1 "
                                     "2.E-3 .5E-6 0.75E-9 1.0E-1 "
                                     "2E1 -2e1 +2e1 5e-1 "
                                    ))

    assert [t.type for t in tokens] == ['float'] * 28
    assert [t.value for t in tokens][0:4] == [2.0, 0.5, 0.75, 10.0]
    assert [t.value for t in tokens][4:8] == [2.0, 0.5, 0.75, 10.0]
    assert [t.value for t in tokens][8:12] == [-2.0, -0.5, -0.75, -10.0]
    assert [t.value for t in tokens][12:16] == [2E3, .5E6, .75E9, 10]
    assert [t.value for t in tokens][16:20] == [2E3, .5E6, .75E9, 10]
    assert [t.value for t in tokens][20:24] == [2E-3, .5E-6, .75E-9, 0.1]
    assert [t.value for t in tokens][24:28] == [20.0, -20.0, 20.0, 0.5]

def test_hex64():
    tokenizer = libconf.Tokenizer("<memory>")

    tokens = list(tokenizer.tokenize("0x13AL 0XbcdL 0xefLL 0X456789ABLL"))

    assert [t.type for t in tokens] == ['hex64'] * 4
    assert [t.value for t in tokens] == [0x13A, 0xBCD, 0xef, 0x456789AB]

def test_hex():
    tokenizer = libconf.Tokenizer("<memory>")

    tokens = list(tokenizer.tokenize("0x13A 0Xbcd 0xef 0X456789AB"))

    assert [t.type for t in tokens] == ['hex'] * 4
    assert [t.value for t in tokens] == [0x13A, 0xBCD, 0xef, 0x456789AB]

def test_integer64():
    tokenizer = libconf.Tokenizer("<memory>")

    tokens = list(tokenizer.tokenize("10L +30L -15000000000LL"))

    assert [t.type for t in tokens] == ['integer64'] * 3
    assert [t.value for t in tokens] == [10, 30, -15000000000]

def test_integer():
    tokenizer = libconf.Tokenizer("<memory>")

    tokens = list(tokenizer.tokenize("10 +30 -15000000000"))

    assert [t.type for t in tokens] == ['integer'] * 3
    assert [t.value for t in tokens] == [10, 30, -15000000000]

def test_boolean():
    tokenizer = libconf.Tokenizer("<memory>")

    tokens = list(tokenizer.tokenize("true TRUE TrUe false FALSE FaLsE"))

    assert [t.type for t in tokens] == ['boolean'] * 6
    assert [t.value for t in tokens] == [True, True, True, False, False, False]

def test_string():
    tokenizer = libconf.Tokenizer("<memory>")

    tokens = list(tokenizer.tokenize(
        r'''"abc" "ab\"cd" "" "\x20\\\f\n\r\t"'''))

    assert [t.type for t in tokens] == ['string'] * 4
    assert [t.value for t in tokens] == ['abc', 'ab"cd', '', ' \\\f\n\r\t']

def test_name():
    tokenizer = libconf.Tokenizer("<memory>")

    tokens = list(tokenizer.tokenize("ident IdenT I I32A"))

    assert [t.type for t in tokens] == ['name'] * 4
    assert [t.text for t in tokens] == ['ident', 'IdenT', 'I', 'I32A']

def test_special():
    tokenizer = libconf.Tokenizer("<memory>")

    tokens = list(tokenizer.tokenize("}]){[(=:,;"))

    assert [t.type for t in tokens] == list("}]){[(=:,;")

def test_location():
    tokenizer = libconf.Tokenizer("<memory>")

    tokens = list(tokenizer.tokenize("\n    0   1\n        2"))

    assert [t.type for t in tokens] == ['integer'] * 3
    assert [(t.row, t.column) for t in tokens] == [(2, 5), (2, 9), (3, 9)]

def test_invalid_token():
    tokenizer = libconf.Tokenizer("<memory>")

    with pytest.raises(libconf.ConfigParseError) as exc_info:
        list(tokenizer.tokenize("\n\n        `xvz"))

    assert '<memory>' in str(exc_info.value)
    assert 'row 3' in str(exc_info.value)
    assert 'column 9' in str(exc_info.value)
    assert '`xvz' in str(exc_info.value)

