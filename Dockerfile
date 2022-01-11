FROM python:3.10

RUN apt-get update && apt-get upgrade -y && apt-get autoremove -y
RUN apt-get install -y \
	pandoc \
	texlive-latex-base \
	texlive-fonts-recommended \
	texlive-fonts-extra \
	texlive-latex-extra \
    curl

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "curl", "-f", "localhost:80/live" ]

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:80", "server:app"]
