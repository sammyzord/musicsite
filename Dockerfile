FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD python3 manage.py migrate && gunicorn -b  0.0.0.0:$PORT musicsite.wsgi