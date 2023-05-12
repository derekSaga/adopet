FROM python:3.9.13-slim
RUN adduser --system --no-create-home nonroot

# Creates application directory
WORKDIR /app

# Creates an appuser and change the ownership of the application's folder
RUN useradd appuser && chown appuser /app

# Installs poetry and pip
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false --local

# Copy dependency definition to cache
COPY --chown=appuser poetry.lock pyproject.toml README.md /app/

# Installs projects dependencies as a separate layer
RUN poetry install --no-root

# Copies and chowns for the userapp on a single layer
COPY --chown=appuser adopet/ /app
COPY --chown=appuser tests/ /app
COPY --chown=appuser scripts/ /app
COPY --chown=appuser logging.yaml /app

USER nonroot
