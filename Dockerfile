FROM python:3.6-alpine as base

LABEL maintainer = "Felix Fennell <felnne@bas.ac.uk>"

ENV APPPATH=/usr/src/app/
ENV PYTHONPATH=$APPPATH

RUN mkdir $APPPATH
WORKDIR $APPPATH

RUN apk add --no-cache libxslt-dev libffi-dev openssl-dev git


FROM base as build

ENV APPVENV=/usr/local/virtualenvs/bas_metadata_library

RUN apk add --no-cache build-base cargo
RUN python3 -m venv $APPVENV
ENV PATH="$APPVENV/bin:$PATH"

# pre-install known wheels to save time
ADD http://bsl-repoa.nerc-bas.ac.uk/magic/v1/libraries/python/wheels/linux_x86_64/cp36m/lxml-4.5.2-cp36-cp36m-linux_x86_64.whl /tmp/wheelhouse/
RUN pip install --no-index --find-links=file:///tmp/wheelhouse lxml==4.5.2

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry==1.0.0

COPY pyproject.toml poetry.toml poetry.lock $APPPATH
RUN poetry install --no-root --no-interaction --no-ansi


FROM base as run

ENV APPVENV=/usr/local/virtualenvs/bas_metadata_library
ENV PATH="$APPVENV/bin:$PATH"
ENV FLASK_APP=/usr/src/app/manage.py
ENV FLASK_ENV=development

COPY --from=build $APPVENV/ $APPVENV/

ENTRYPOINT []
