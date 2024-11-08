# FBA Project - Backend

## Docker

> [!IMPORTANT]
> Due to Docker context limitations, you cannot successfully build a image using a Dockerfile in the current directory

1. Make sure you're at the root of the project
2. Run the following Docker command to build a image:

   ```shell
   docker build -f backend/backend.dockerfile -t fba_backend_independent .
   ```

3. Start decker image

   ```shell
   docker run -d fba_backend_independent -p 8000:8000 --name fba_app
   ```

## Contributing

1. Prerequisites

   You'll need the following prerequisites:
    - Any Python version between Python >= 3.10
    - virtualenv or other virtual environment tool
    - git
    - [uv](https://docs.astral.sh/uv/getting-started/installation/)

2. Installation and setup

   ```shell
   # Clone your fork and cd into the repo directory
   git clone https://github.com/<your username>/fastapi_best_architecture.git
   
   cd fastapi_best_architecture/backend
   
   vv venv
   
   uv pip install -r requirements.txt
   ```

3. Check out a new branch and make your changes

   ```shell
   # Checkout a new branch and make your changes
   git checkout -b your-new-feature-branch
   # Make your changes...
   ```

4. Run linting

   ```shell
   # Run automated code formatting and linting
   pre-commit run --all-files
   ```

5. Commit and push your changes

   Commit your changes, push your branch to GitHub, and create a pull request.

## Scripts

> [!WARNING]
>
> The following script may not apply to the Windows platform
>
> It is recommended to execute under the backend directory, and chmod authorization may be required

- `pre_start.sh`: Perform automatic database migration and create database tables

- `celery-start.sh`: For celery docker script, implementation is not recommended

- `scripts/format.sh`: Perform ruff format check

- `scripts/lint.sh`: Perform pre-commit formatting

- `scripts/export.sh`: Execute uv export dependency package
