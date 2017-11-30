FROM python:2.7
WORKDIR /app
COPY app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY scripts/wait-for-mongo.sh /wait-for-mongo.sh
COPY app /app
ENV MONGODB_HOST db