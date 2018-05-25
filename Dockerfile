FROM python:3.6-alpine

ENV FLASK_APP app.py
WORKDIR /app
ADD app.py .
ADD requirements.txt .

RUN pip install -r requirements.txt

CMD flask run --host=0.0.0.0
