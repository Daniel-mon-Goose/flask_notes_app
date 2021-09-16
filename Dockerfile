FROM python:3.9-alpine

RUN adduser -D notes_app

WORKDIR /home/notes_app

RUN apk add build-base
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY notes.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP notes.py

RUN chown -R notes_app:notes_app ./
USER notes_app

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]