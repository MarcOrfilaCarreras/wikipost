FROM python:3.10-slim

WORKDIR /app

COPY ./requirements-dev.txt /app/requirements-dev.txt
COPY ./requirements.txt /app/requirements.txt

COPY . /app

RUN apt update -y && apt-get install fonts-dejavu git -y
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV FLASK_APP=app.py

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8080", "--timeout", "120", "wsgi:app"]
