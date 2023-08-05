example_pkg_cloos
=================

.. image:: https://img.shields.io/pypi/v/example_pkg_cloos.svg
   :target: https://pypi.org/project/example-pkg-cloos/

.. image:: https://img.shields.io/pypi/l/example_pkg_cloos.svg
   :target: https://pypi.org/project/example-pkg-cloos/

.. image:: https://img.shields.io/pypi/pyversions/example_pkg_cloos.svg
   :target: https://pypi.org/project/example-pkg-cloos/

.. image:: https://img.shields.io/travis/cloos/python_example_pkg_cloos/master.svg
   :target: https://travis-ci.org/cloos/python_example_pkg_cloos/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
   :alt: Code style: black

A example package to learn and test Python packaging.

https://packaging.python.org/tutorials/packaging-projects/

Development workflow
--------------------

Checkout git repository:

.. code:: shell

   $ git clone git@github.com:cloos/python_example_pkg_cloos.git

Create virtualenv:

.. code:: shell

   $ make venv

Activate virtualenv:

.. code:: shell

   $ source venv/bin/activate

Install/Upgrade packaging tools:

.. code:: shell

   $ make install

Install package in 'development mode':

.. code:: shell

   $ make develop

Run tests:

.. code:: shell

    $ make test

Create Git tag:

.. code:: shell

   $ git tag -m "release 0.0.1" 0.0.1
   $ git push --tags

Upload to https://test.pypi.org/:

.. code:: shell

   $ make upload_test

Upload to https://pypi.org/:

.. code:: shell

   $ make upload

Usage
-----

.. code:: shell

   $ pip install example-pkg-cloos

Cli:

.. code:: shell

   example-pkg-cloos --help

Library:

.. code:: python

   from example_pkg_cloos.utils import print_bar, print_foo

   print_bar()
   print_foo()
