FROM python:3

RUN mkdir -p /app

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt > server.log

ENV FLASK_APP server/server.py
ENV CLOUDINARY_URL cloudinary://738462148762527:t9Jri_atBqGG7yJkmqHmTmKY_V4@du95usvl0

RUN flask db init > server.log && \
    flask db migrate > server.log && \
    flask db upgrade > server.log

EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
