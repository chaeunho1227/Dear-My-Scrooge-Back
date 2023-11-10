FROM python:3.11-slim
WORKDIR /app
COPY ./requirements.txt requirements.txt

RUN pip install --upgrade pip &&\
    pip install -r requirements.txt

COPY . .

RUN python manage.py makemigrations &&\
    python manage.py makemigrations main &&\
    python manage.py makemigrations users &&\
    python manage.py migrate && \
    pip install gunicorn

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:8000 Scrooge.wsgi:application"]