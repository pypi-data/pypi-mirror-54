About
=====

Console app and Python API for automated assignment examination of our `ACS`_
students.

.. _`ACS`: http://www.acs.uns.ac.rs/

Installation
============

To install acs_examine_student_assignment run::

    $ pip install acs_examine_student_assignment

Console app usage
=================

Quick start::

    $ acs_examine_student_assignment <computer>

Show help::

    $ acs_examine_student_assignment --help

Python API usage
================

Quick start::

    >>> import logging
    >>> logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")

    >>> from acs_examine_student_assignment import examine_student_assignment
    >>> examine_student_assignment('extracted', 's200')


Contribute
==========

If you find any bugs, or wish to propose new features `please let us know`_.

If you'd like to contribute, simply fork `the repository`_, commit your changes
and send a pull request. Make sure you add yourself to `AUTHORS`_.

.. _`please let us know`: https://github.com/petarmaric/acs_examine_student_assignment/issues/new
.. _`the repository`: https://github.com/petarmaric/acs_examine_student_assignment
.. _`AUTHORS`: https://github.com/petarmaric/acs_examine_student_assignment/blob/master/AUTHORS
