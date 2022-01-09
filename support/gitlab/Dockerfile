FROM python:3.6-alpine as base

LABEL maintainer = "Felix Fennell <felnne@bas.ac.uk>"

RUN apk add --no-cache build-base libxslt-dev libffi-dev openssl-dev libxml2-utils cargo

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry
