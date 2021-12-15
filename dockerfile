FROM tiangolo/uwsgi-nginx-flask:python3.6

RUN pip install -U pip
RUN pip install Flask psycopg2
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./app /app

