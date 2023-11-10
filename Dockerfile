FROM python:3.11
WORKDIR /app
COPY ./requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py makemigrations

RUN pip install gunicorn

CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 Scrooge.wsgi:application"]