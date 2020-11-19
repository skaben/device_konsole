FROM python:3.7-slim
MAINTAINER zerthmonk

ENV PYTHONUBUFFERED=1
ENV PATH="/venv/bin:$PATH"

COPY build_requirements.txt /build_requirements.txt

ENV VENV="/venv"
RUN python -m venv $VENV
ENV PATH="$VENV/bin:$PATH"

RUN python -m pip install --upgrade pip && \
    python -m pip install -r /build_requirements.txt

RUN mkdir /app
WORKDIR /app

