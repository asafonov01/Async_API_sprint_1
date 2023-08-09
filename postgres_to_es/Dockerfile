FROM python:3.10-slim

WORKDIR /postgres_to_es

RUN apt-get update && apt-get install -y curl && apt-get install -y netcat-traditional

COPY ./postgres_to_es/requirements.txt /

RUN  pip install --upgrade pip \ 
     && pip install -r /requirements.txt 

COPY ./postgres_to_es/ ./

ENTRYPOINT ["sh", "entrypoint.sh"]
