Pursue
======

.. image:: http://img.shields.io/pypi/v/pursue.svg
    :target: https://pypi.python.org/pypi/pursue
    :alt: Latest version

.. image:: http://img.shields.io/pypi/dm/pursue.svg
    :target: https://pypi.python.org/pypi/pursue
    :alt: Number of PyPI downloads

.. image:: https://secure.travis-ci.org/jaimegildesagredo/pursue.svg?branch=master
    :target: http://travis-ci.org/jaimegildesagredo/pursue

OpenStack Object Storage Python Client featuring client-side object encryption.

Installation
------------

.. code-block:: bash

    $ git clone https://github.com/jaimegildesagredo/pursue.git
    $ cd pursue
    $ python setup.py install && pip install -r requirements.txt

Usage
-----

.. code-block:: bash

    $ pursue --help
    Pursue - OpenStack Object Storage client

    Usage:
        pursue [options] list [<container>]
        pursue [options] upload <container> <path>
        pursue [options] download <container> <object>
        pursue [options] delete <container> [<object>]
        pursue [options] keygen <path>

    Options:
        -h --help   Shows these lines.
        --account-name <account_name>
        --auth-token <auth_token>
        --secret <path>
