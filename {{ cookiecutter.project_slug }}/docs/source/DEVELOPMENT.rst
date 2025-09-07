
Development Guide
=================

Contents:

- Setup
- Running the Application
- Configuration
- Database Migrations
- Translations
- CI/CD

Setup
-----

1. Clone the repository.
2. Copy ``.env.example`` to ``.env`` and configure environment variables.

Running the Application
-----------------------

Locally:

.. code-block:: shell

   python3 app/main.py

With Docker:

.. code-block:: shell

   docker-compose up -d

Configuration
-------------

Settings are in ``app/config/components/``. Switch environments via ``ENVIRONMENT`` in ``.env``.

Database Migrations
-------------------

Uses Tortoise ORM and Aerich.

- Init:

  .. code-block:: shell

     aerich init-db

- New migration:

  .. code-block:: shell

     aerich migrate

- Apply:

  .. code-block:: shell

     aerich upgrade

Translations
------------

Uses FastAPI-Babel and Pybabel.

- Extract:

  .. code-block:: shell

     make translations-extract

- Init language:

  .. code-block:: shell

     make translations-init LANG=xx

- Compile:

  .. code-block:: shell

     make translations-compile

- Update:

  .. code-block:: shell

     make translations-update

- Full process:

  .. code-block:: shell

     make translations-all LANG=xx

Directory structure:

- ``/app/locales/``: All translations
- ``messages.pot``: Template
- ``<lang>/LC_MESSAGES/``: Translated files

In code:

.. code-block:: python

   from fastapi_babel import _
   message = _("Your message")

CI/CD
-----

GitLab CI pipeline defined in ``.gitlab-ci.yml``.
