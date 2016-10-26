=======
libconf
=======

libconf is a pure-Python reader/writer for configuration files in `libconfig
format`_, which is often used in C/C++ projects. It's interface is similar to
the `json`_ module: the four main methods are ``load()``, ``loads()``,
``dump()``, and ``dumps()``.

Example usage::

    import libconf
    >>> with open('example.cfg') as f:
    ...     config = libconf.load(f)
    >>> config
    {'capabilities': {'can-do-arrays': [3, 'yes', True],
                      'can-do-lists': (True,
                                       14880,
                                       ('sublist',),
                                       {'subgroup': 'ok'})},
     'version': 7,
     'window': {'position': {'h': 600, 'w': 800, 'x': 375, 'y': 210},
                'title': 'libconfig example'}}

    >>> config['window']['title']
    'libconfig example'
    >>> config.window.title
    'libconfig example'

    >>> print(libconf.dumps({'size': [10, 15], 'flag': True}))
    flag = True;
    size =
    [
        10,
        15
    ];

The data can be accessed either via indexing (``['title']``) or via attribute
access ``.title``.

Character encoding and escape sequences
---------------------------------------

The recommended way to use libconf is with Unicode objects (``unicode`` on
Python2, ``str`` on Python3). Input strings or streams for ``load()`` and
``loads()`` should be Unicode, as should be all strings contained in data
structures passed to ``dump()`` and ``dumps()``.

In ``load()`` and ``loads()``, escape sequences (such as ``\n``, ``\r``,
``\t``, or ``\xNN``) are decoded. Hex escapes (``\xNN``) are mapped to Unicode
characters U+0000 through U+00FF. All other characters are passed though as-is.

In ``dump()`` and ``dumps()``, unprintable characters below U+0080 are escaped
as ``\n``, ``\r``, ``\t``, ``\f``, or ``\xNN`` sequences. Characters U+0080
and above are passed through as-is.

Comparison to other Python libconfig libraries
----------------------------------------------

`Pylibconfig2`_ is another pure-Python libconfig reader. It's API
is based on the C++ interface, instead of the Python `json`_ module.
It's licensed under GPLv3, which makes it unsuitable for use in a large number
of projects.

`Python-libconfig`_ is a library that provides Python bindings for the
libconfig++ C++ library. While permissively licensed (BSD), it requires a
compilation step upon installation, which can be a drawback.

I wrote libconf (this library) because both of the existing libraries didn't
fit my requirements. I had a work-related project which is not open source
(ruling out pylibconfig2) and I didn't want the deployment headache of
python-libconfig. Further, I enjoy writing parsers and this seemed like a nice
opportunity :-)

.. _libconfig format: http://www.hyperrealm.com/libconfig/libconfig_manual.html#Configuration-Files
.. _json: https://docs.python.org/3/library/json.html
.. _Pylibconfig2: https://github.com/heinzK1X/pylibconfig2
.. _Python-libconfig: https://github.com/cnangel/python-libconfig
