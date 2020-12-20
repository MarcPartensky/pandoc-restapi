FROM python:3.8-alpine

RUN apk update
RUN apk add git jpeg-dev zlib-dev libjpeg libffi-dev gcc build-base python3-dev musl-dev pdf2latex

COPY requirements.txt /

RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app
EXPOSE 5000

ENTRYPOINT ["flask", "run"]
