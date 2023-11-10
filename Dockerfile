FROM python:3.11-slim
WORKDIR /app
COPY ./requirements.txt requirements.txt

RUN pip install --upgrade pip &&\
    pip install -r requirements.txt &&\
    pip install gunicorn

COPY . .

CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 Scrooge.wsgi:application"]