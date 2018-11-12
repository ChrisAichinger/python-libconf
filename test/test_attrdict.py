import libconf


# Tests for AttrDict behavior
#############################

def test_attrdict_hasattr():
    d = libconf.AttrDict()
    assert hasattr(d, 'no_such_attr') == False
