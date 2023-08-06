========
Overview
========

Python Library to work with Qlik API

* Free software: Apache Software License 2.0

v0.2.4.

Installation
============

::

    pip install paralelocs-qlikapi

You can also install the in-development version with::

    pip install git+ssh://git@paralelo/pyqlikapi/.git@master

Documentation
=============


To use the project:

.. code-block:: python

    import paralelocs_qlikapi
    paralelocs_qlikapi.longest()


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
