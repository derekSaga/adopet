FROM python:3.9.13


# Creates application directory
WORKDIR /app

# Creates an appuser and change the ownership of the application's folder
RUN useradd appuser
RUN chown -R appuser /app

# Installs poetry and pip
RUN pip install --upgrade pip
RUN pip install poetry

# Copy dependency definition to cache
COPY --chown=appuser poetry.lock pyproject.toml /app/

# Installs projects dependencies as a separate layer
RUN poetry export -o requirements.txt -f requirements.txt --no-cache
RUN pip uninstall --yes poetry
RUN pip install --require-hashes --no-cache-dir -R requirements.txt

# Copies and chowns for the userapp on a single layer
COPY --chown=appuser adopet/ .

# Switching to the non-root appuser for security
USER appuser