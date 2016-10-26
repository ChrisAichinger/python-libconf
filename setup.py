from setuptools import setup

setup(
    name='libconf',
    version='1.0.0',
    description="A pure-Python libconfig reader/writer with permissive license",
    long_description=open('README.rst').read(),
    author="Christian Aichinger",
    author_email="Greek0@gmx.net",
    url='https://github.com/Grk0/python-libconf',
    download_url='https://github.com/Grk0/python-libconf/tarball/1.0.0',
    license="MIT",
    py_modules=['libconf'],
    keywords='libconfig configuration parser library',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
