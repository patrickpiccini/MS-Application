FROM python:3.8-alpine
COPY . /app/
ENV HOST='10.0.0.25'
ENV HOST_DATABASE='10.5.0.11'

ENV CACHE_TYPE='redis' 
ENV CACHE_REDIS_HOST='10.0.0.25'
ENV CACHE_REDIS_PORT='6379' 
ENV CACHE_REDIS_DB=0 

EXPOSE 7000
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD python server.py