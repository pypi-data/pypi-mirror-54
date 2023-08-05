========
Overview
========

Paraleo CS Custom packages to work with Apache Beam on Python SDK

* Free software: Apache Software License 2.0

Installation
============

::

    pip install paralelocs-beam

You can also install the in-development version with::

    pip install git+ssh://git@https://gitlab.com/paralelo/lucasmagalhaes/paralelocs_beam.git@master

Documentation
=============


To use the project:

.. code-block:: python

    import paralelocs_beam
    paralelocs_beam.longest()


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
