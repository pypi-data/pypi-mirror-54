######
scaffy
######

.. readme_inclusion_marker

**scaffy** is a small tool to create, manage and apply project scaffolds (or
any directory scaffold for that matter). It includes a web service that allows
storing the scaffolds remotely.

Installation
============

.. code-block:: shell

    $ pip install scaffy

Usage
=====


Contributing
============

Principal rule
--------------

**Make it work, then make it right, then make it fast.**

Setting up development repo
---------------------------

.. code-block:: shell

    $ git clone git@github.com:novopl/scaffy.git
    $ cd scaffy
    $ virtualenv env
    $ source ./env/bin/activate
    $ python setup.py develop
    $ pip install -r ops/devrequirements.txt

The project uses **peltak** for management. See
`peltak <https://github.com/novopl/peltak>`_ docs for more information.
