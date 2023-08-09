FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-traditional

COPY ./movies_admin/requirements.txt /

RUN  pip install --upgrade pip \ 
     && pip install -r /requirements.txt 

COPY ./movies_admin/entrypoint.sh ./
COPY ./movies_admin/gunicorn.conf.py ./
COPY ./movies_admin ./

EXPOSE 8000

ENTRYPOINT ["sh", "entrypoint.sh" ]
