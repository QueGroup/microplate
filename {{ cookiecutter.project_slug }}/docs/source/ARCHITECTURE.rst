.. _architecture:

Architecture
============

Contents:

- Architecture
- Installation

  - Create repository from a template
  - Install dependencies
  - Configure environment variables
  - Setup development stand
  - Aliases
- License

Architecture Overview
---------------------

This template follows the **Clean Architecture** principles, which separate the application into four main layers:

1. **Domain Layer**

   - Contains the core business logic and entities.
   - Located in ``src/application/<module>/domain/``.
   - Key components:

     - **Entities**: Core business objects (e.g., ``entity.py``)
     - **Value Objects**: Immutable objects that represent values (e.g., ``value_objects.py``)
     - **Events**: Domain events representing significant changes (e.g., ``event.py``)
     - **Interfaces**: Contracts for external systems (e.g., ``interfaces.py``)

2. **Application Layer**

   - Orchestrates the business logic and interacts with the domain layer.
   - Located in ``src/application/<module>/``.
   - Key components:

     - **Interactors**: Implement use cases (e.g., ``interactors/``)
     - **DTOs**: Data Transfer Objects (e.g., ``dto.py``)
     - **Mappers**: Data converters (e.g., ``mappers.py``)
     - **Exceptions**: Custom exceptions (e.g., ``exceptions.py``)

3. **Infrastructure Layer**

   - Implements integrations with external systems.
   - Located in ``src/infrastructure/``.
   - Key components:

     - **Database**: Models, migrations, repositories (e.g., ``db/``)
     - **External Services**: API clients, etc. (e.g., ``external/``)
     - **IoC**: Dependency injection setup (e.g., ``ioc/``)
     - **Logging**: Logging configuration (e.g., ``log/``)

4. **Presentation Layer**

   - Manages user interaction and APIs.
   - Located in ``src/presentation/``.
   - Key components:

     - **API Controllers**: Handle requests/responses (e.g., ``controllers.py``)
     - **Middlewares**: Request/response processing (e.g., ``middlewares/``)
     - **Metrics**: Monitoring tools (e.g., ``metrics.py``)

Installation
------------

1. Create Repository from Template

   Click the "Use this template" button on GitHub.

2. Install Dependencies

   First, install `uv`, then run:

   .. code-block:: shell

      uv sync

3. Configure Environment Variables

   Copy `.env.template` to `.env` and fill it in:

   .. code-block:: shell

      just create_env

   +------------------------------+--------------------------------------------------------+----------+----------+
   | Variable Name               | Description                                            | Required | Type     |
   +==============================+========================================================+==========+==========+
   | POSTGRES_DB                 | Name of the PostgreSQL database.                      | Yes      | string   |
   | POSTGRES_USER               | Database username.                                    | Yes      | string   |
   | POSTGRES_HOST               | Host address of PostgreSQL.                           | Yes      | string   |
   | POSTGRES_PORT               | Port number for PostgreSQL.                           | Yes      | number   |
   | POSTGRES_PASSWORD           | Password for database.                                | Yes      | string   |
   | REDIS_PORT                  | Redis server port.                                    | Yes      | number   |
   | REDIS_HOST                  | Redis server host.                                    | Yes      | string   |
   | OTEL_EXPORTER_OTLP_ENABLED  | Enable OpenTelemetry exporter.                        | Yes      | boolean  |
   +------------------------------+--------------------------------------------------------+----------+----------+

4. Setup Development Stand

   Start services with Docker:

   .. code-block:: shell

      docker-compose up -d

5. Aliases

   Run ``just help`` to see available shortcuts. This project uses ``just`` for command aliases.

License
-------

This project is licensed under the MIT License. See ``LICENSE`` file for details.
