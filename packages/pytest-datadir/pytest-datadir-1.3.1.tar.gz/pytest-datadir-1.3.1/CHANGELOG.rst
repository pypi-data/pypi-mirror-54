pytest-datadir
==============

1.3.1 (2019-10-22)
------------------

- Add testing for Python 3.7 and 3.8.
- Add ``python_requires`` to ``setup.py`` so ``pip`` will not try to install ``pytest-datadir`` in incompatible Python versions.


1.3.0 (2019-01-15)
------------------

- Add support for long path names on Windows (`#25 <https://github.com/gabrielcnr/pytest-datadir/pull/25>`__).


1.2.1 (2018-07-12)
------------------

- Fix ``pytest_datadir.version`` attribute to point to the correct version.


1.2.0 (2018-07-11)
------------------

- Use ``pathlib2`` on Python 2.7: this is the proper backport of Python 3's standard
  library.

1.1.0 (2018-07-10)
------------------

- If the data directory does not exist, the fixture will create an empty directory.

1.0.1 (2017-08-15)
------------------

**Fixes**

- Fixed ``shared_datadir`` contents not being copied to a temp location on each test. `#12
  <https://github.com/gabrielcnr/pytest-datadir/issues/12>`_
