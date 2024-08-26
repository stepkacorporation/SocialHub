# SocialHub

**SocialHub** - an asynchronous API built with FastAPI for managing social profiles.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
  - [Development Environment](#development-environment)
  - [Stopping the Development Containers](#stopping-the-development-containers)
- [Running Tests](#running-tests)
  - [Testing Environment](#testing-environment)
- [API Documentation](#api-documentation)

## Features

- **User Registration**: Register users with fields for email, password, username, date of birth, and phone number.
- **User Authentication**: Authenticate users via email and password using JWT.
- **Profile Management:**
  - Link any number of social media accounts to the user profile.
  - Manage (create, read, update, delete) linked social media profiles.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/stepkacorporation/SocialHub.git
    cd SocialHub
    ```

2. **Configure Environment Files**

Create and configure the necessary environment files. You'll need two files:

- `.env.dev` for development
- `.env.test` for testing
   
**For Development:**

Create a `.env.dev` file in the root directory with the following format:

```env
POSTGRES_USER=socialhub
POSTGRES_PASSWORD=your_posgres_password
POSTGRES_DB=socialhub
POSTGRES_HOST=postgres-dev
POSTGRES_PORT=5432
```

Replace the placeholders with your PostgreSQL credentials.

**For Testing:**

Create a `.env.test` file with the same format as above. You might want to use different credentials or database configurations for testing.

```env
POSTGRES_USER=socialhub
POSTGRES_PASSWORD=your_posgres_password
POSTGRES_DB=test_socialhub
POSTGRES_HOST=postgres-test
POSTGRES_PORT=5432
```
   
## Running the Application

### Development Environment

To start the development containers and run the application, use:

```bash
./scripts/run-dev.sh [OPTIONS]
```

- `-d` or `--detach`: Run containers in the background.
- `--build`: Rebuild the images before starting the containers.
- `-f <file>`: Specify an alternative Docker Compose file.

**Examples**

- Start development containers in the background:

  ```bash
  ./scripts/run-dev.sh -d
  ```

- Rebuild images and start containers in the background:

  ```bash
  ./scripts/run-dev.sh -d --build
  ```

### Stopping the Development Containers

To stop and remove the development containers, use:

```bash
./scripts/stop-dev.sh [OPTIONS]
```

- `-v` or `--volumes`: Remove associated volumes in addition to stopping and removing containers.

**Examples**

- Stop and remove containers:

  ```bash
  ./scripts/stop-dev.sh
  ```

- Stop, remove containers, and delete volumes:

  ```bash
  ./scripts/stop-dev.sh -v
  ```


## Running Tests

### Testing Environment

To run the tests, use:

```bash
./scripts/run-tests.sh [TEST_ARGS]
```

- `TEST_ARGS`: Arguments to pass to pytest (e.g., -vv for verbose output).

**Examples**

- Run tests with verbose output:

  ```bash
  ./scripts/run-tests.sh -vv
  ```

This script will start the containers needed for testing, execute the tests, and then stop and remove the test containers using the configuration from `.env.test`.

## API Documentation

The API documentation is automatically generated and available at:

- [http://localhost:8000/docs](http://localhost:8000/docs)
- [http://localhost:8000/redoc](http://localhost:8000/redoc)

This provides an interactive interface for exploring and testing the API endpoints.