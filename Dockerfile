FROM python:2.7
COPY app/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
RUN apt-get update && apt-get install -y netcat
COPY app /app
COPY scripts /scripts
COPY tests /tests