
Mail Relay
.. image:: https://circleci.com/gh/samantehrani/mail-relay.svg?circle-token=3af48550b9a47883ad9f13b1060ddf6a3fa1ac41
   :target: https://circleci.com/gh/samantehrani/mail-relay
   :alt: CircleCI

=========================================================================================================================================================================================================================

Mail Relay is a python tool that


* uses **Export Group** of an organization to **decrypt** PreVeil encrypted emails
* and **relays** them to a configurable IMAP or SMTP destination.

Install
-------

Currently py27 is the only supported python version. It is recommended that you install this tool within a fresh virtual environment. More info on https://virtualenv.pypa.io/en/stable/userguide/.

.. code-block:: shell

   > cd ${repo_root}
   > ${envpip} install -r requirements.txt -r requirements_${osx/linux}.txt
   > ${envpip} install .

Usage
-----

Mail relay exposes a command line interface relay, with which you can configure and initialize the relay process.

.. code-block:: shell

   > relay [OPTIONS] COMMAND [ARGS]
   > relay --help # inspect full list of options/commands/arguments

Testing
-------

We use `tox <https://tox.readthedocs.io/en/latest/index.html>`_ as the project's test runner. Make sure you have **tox >= 3.5.3** installed in your python environment.

Run all tests
~~~~~~~~~~~~~

.. code-block:: shell

   > cd ${repo_core}
   >   tox

Unit tests
~~~~~~~~~~

.. code-block:: shell

   >   tox -e unit-${osx/linux}

Integration tests
~~~~~~~~~~~~~~~~~

.. code-block:: shell

   > tox -e integration-${osx/linux}

Linting
-------

We use `flake8 <http://flake8.pycqa.org/en/latest/>`_ as project's linter. Enforcement via:

.. code-block:: shell

   >   tox -e flake8
