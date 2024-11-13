FROM python:3.11.2

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

WORKDIR /app/NBA_scraper

CMD [ "bash" ]

