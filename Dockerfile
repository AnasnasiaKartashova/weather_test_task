FROM python:3.11

ENV PYTHONUNBUFFERED=TRUE

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip &&  pip3 install -r ./requirements.txt --no-cache-dir
RUN pip install gunicorn

COPY ./ /app