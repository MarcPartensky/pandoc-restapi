FROM python:3.10

RUN apt-get update
RUN apt-get install -y \
	pandoc \
	texlive-latex-base \
	texlive-fonts-recommended \
	texlive-fonts-extra \
	texlive-latex-extra

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:80", "server:app"]
