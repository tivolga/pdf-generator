FROM python:3.7.5-slim

WORKDIR /usr/local/pdf-creator

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY python python
COPY fonts fonts
COPY images images
COPY config.txt .

COPY templates templates

COPY static static

EXPOSE 5050:5050

CMD python python/runner.py
