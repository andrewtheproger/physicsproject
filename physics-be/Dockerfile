FROM python:3

RUN pip install flask flask_sqlalchemy flask_migrate
RUN mkdir -p /app

WORKDIR /app
COPY . /app

ENV FLASK_APP server.py

RUN flask db init && \
    flask db migrate && \
    flask db upgrade

EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
