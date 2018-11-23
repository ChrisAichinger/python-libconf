=======
libconf
=======

libconf is a pure-Python reader/writer for configuration files in `libconfig
format`_, which is often used in C/C++ projects. It's interface is similar to
the `json`_ module: the four main methods are ``load()``, ``loads()``,
``dump()``, and ``dumps()``.

Example usage::

    import io, libconf
    >>> with io.open('example.cfg') as f:
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


Writing libconfig files
-----------------------

Reading libconfig files is easy. Writing is made harder by two factors:

* libconfig's distinction between `int and int64`_: ``2`` vs. ``2L``
* libconfig's distinction between `lists`_ and `arrays`_, and
  the limitations on arrays

The first point concerns writing Python ``int`` values. Libconf dumps values
that fit within the C/C++ 32bit ``int`` range without an "L" suffix. For larger
values, an "L" suffix is automatically added. To force the addition of an "L"
suffix even for numbers within the 32 bit integer range, wrap the integer in a
``LibconfInt64`` class.

Examples::

    dumps({'value': 2})                # Returns "value = 2;"
    dumps({'value': 2**32})            # Returns "value = 4294967296L;"
    dumps({'value': LibconfInt64(2)})  # Explicit int64, returns "value = 2L;"

The second complication arises from distinction between `lists`_ and `arrays`_
in the libconfig language. Lists are enclosed by ``()`` parenthesis, and can
contain arbitrary values within them. Arrays are enclosed by ``[]`` brackets,
and have significant limitations: all values must be scalar (int, float, bool,
string) and must be of the same type.

Libconf uses the following convention:

* it maps libconfig ``()``-lists to Python tuples, which also use the ``()``
  syntax.
* it maps libconfig ``[]``-arrays to Python lists, which also use the ``[]``
  syntax.

This provides nice symmetry between the two languages, but has the drawback
that dumping Python lists inherits the limitations of libconfig's arrays.
To explicitly control whether lists or arrays are dumped, wrap the Python
list/tuple in a ``LibconfList`` or ``LibconfArray``.

Examples::

    # Libconfig lists (=Python tuples) can contain arbitrary complex types:
    dumps({'libconf_list': (1, True, {})})

    # Libconfig arrays (=Python lists) must contain scalars of the same type:
    dumps({'libconf_array': [1, 2, 3]})

    # Equivalent, but more explit by using LibconfList/LibconfArray:
    dumps({'libconf_list': LibconfList([1, True, {}])})
    dumps({'libconf_array': LibconfArray([1, 2, 3])})


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

Release notes
-------------

* **1.0.1**, released on 2017-01-06

  - Drastically improve performance when reading larger files
  - Several smaller improvements and fixes

* **1.0.0**, released on 2016-10-26:

  - Add the ability to write libconf files (``dump()`` and ``dumps()``,
    thanks clarkli86 and eatsan)
  - Several smaller improvements and fixes

* **0.9.2**, released on 2016-09-09:

  - Fix compatibility with Python versions older than 2.7.6 (thanks AnandTella)


.. _libconfig format: http://www.hyperrealm.com/libconfig/libconfig_manual.html#Configuration-Files
.. _json: https://docs.python.org/3/library/json.html
.. _lists: https://hyperrealm.github.io/libconfig/libconfig_manual.html#Lists
.. _arrays: https://hyperrealm.github.io/libconfig/libconfig_manual.html#Arrays
.. _int and int64: https://hyperrealm.github.io/libconfig/libconfig_manual.html#g_t64_002dbit-Integer-Values
.. _Pylibconfig2: https://github.com/heinzK1X/pylibconfig2
.. _Python-libconfig: https://github.com/cnangel/python-libconfig
