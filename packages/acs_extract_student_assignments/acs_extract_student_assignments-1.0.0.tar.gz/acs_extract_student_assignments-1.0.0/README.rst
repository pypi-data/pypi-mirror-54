About
=====

Console app and Python API for extracting assignments from exam archives of our
`ACS`_ students.

.. _`ACS`: http://www.acs.uns.ac.rs/

Installation
============

To install acs_extract_student_assignments run::

    $ pip install acs_extract_student_assignments

Console app usage
=================

Quick start::

    $ acs_extract_student_assignments

Show help::

    $ acs_extract_student_assignments --help

Python API usage
================

Quick start::

    >>> import logging
    >>> logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")

    >>> from acs_extract_student_assignments import find_student_assignments, store_student_assignments
    >>> student_assignments = find_student_assignments('archives')
    >>> store_student_assignments(student_assignments, 'extracted')


Contribute
==========

If you find any bugs, or wish to propose new features `please let us know`_.

If you'd like to contribute, simply fork `the repository`_, commit your changes
and send a pull request. Make sure you add yourself to `AUTHORS`_.

.. _`please let us know`: https://github.com/petarmaric/acs_extract_student_assignments/issues/new
.. _`the repository`: https://github.com/petarmaric/acs_extract_student_assignments
.. _`AUTHORS`: https://github.com/petarmaric/acs_extract_student_assignments/blob/master/AUTHORS
