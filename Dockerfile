FROM python:2.7
COPY ./app /app
WORKDIR /app
RUN pip install -r requirements.txt