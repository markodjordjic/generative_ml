FROM python:3.11-slim

WORKDIR /opt

COPY app ./app
COPY operations ./operations
COPY utilities ./utilities
COPY .env ./

COPY requirements.txt ./requirements.txt

RUN pip install  -r requirements.txt

ENV PYTHONPATH="app/"