FROM python:3.11
WORKDIR /app
COPY ./requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py makemigrations
RUN python manage.py migrate

RUN pip install gunicorn

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:8000 Scrooge.wsgi:application"]