FROM python:3.8

RUN apt-get update

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn", "--bind", "pandoc:80", "server:app"]
