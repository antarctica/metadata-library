FROM python:3.6-alpine as base

LABEL maintainer = "Felix Fennell <felnne@bas.ac.uk>"

RUN apk add --update --no-cache libxslt-dev libffi-dev openssl-dev libxml2-utils

FROM base as build

RUN apk add --update --no-cache build-base cargo curl
RUN python3 -m pip install pipx
RUN python3 -m pipx install poetry==1.1.4

ENV PATH="/root/.local/bin:$PATH"
COPY pyproject.toml poetry.lock /
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-root --no-interaction --no-ansi

FROM base as run

COPY --from=build /root/.local/pipx/venvs/poetry /root/.local/pipx/venvs/poetry
COPY --from=build /root/.local/bin/poetry /root/.local/bin/poetry
COPY --from=build /.venv/ /.venv
ENV PATH="/venv/bin:/root/.local/bin:$PATH"
RUN poetry config virtualenvs.in-project true
ENTRYPOINT []
