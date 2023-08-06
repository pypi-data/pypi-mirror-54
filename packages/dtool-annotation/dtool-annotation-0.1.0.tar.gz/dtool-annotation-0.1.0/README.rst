dtool CLI commands for working with per dataset metadata (annotations)
======================================================================

.. image:: https://badge.fury.io/py/dtool-annotation.svg
   :target: http://badge.fury.io/py/dtool-annotation
   :alt: PyPi package

.. image:: https://travis-ci.org/jic-dtool/dtool-annotation.svg?branch=master
   :target: https://travis-ci.org/jic-dtool/dtool-annotation
   :alt: Travis CI build status (Linux)

.. image:: https://codecov.io/github/jic-dtool/dtool-annotation/coverage.svg?branch=master
   :target: https://codecov.io/github/jic-dtool/dtool-annotation?branch=master
   :alt: Code Coverage


Installation
------------

::

    $ pip install dtool-annotation


Example usage
-------------

Get a dataset to play with::

    $ LOCAL_DS_URI=$(dtool cp -q http://bit.ly/Ecoli-ref-genome .)


Add an annotation::

    $ dtool annotation set $LOCAL_DS_URI project dtool-demo

Get an annotation::

    $ dtool annotation get $LOCAL_DS_URI project
    dtool-demo

Add an annotation forcing a specific type::

    $ dtool annotation set --type int $LOCAL_DS_URI stars 3

List all annotations::

    $ dtool annotation ls
    project dtool-demo
    stars   3

For more information see the `dtool documentation <https://dtool.readthedocs.io>`_.

Related packages
----------------

- `dtoolcore <https://github.com/jic-dtool/dtoolcore>`_
- `dtool-cli <https://github.com/jic-dtool/dtool-cli>`_
- `dtool-create <https://github.com/jic-dtool/dtool-create>`_
- `dtool-overlay <https://github.com/jic-dtool/dtool-overlay>`_
