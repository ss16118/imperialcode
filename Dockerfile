FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code && \
    apt-get install -y ruby && \
    apt install libpq-dev python3-dev
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

EXPOSE 5000
CMD gunicorn --bind 0.0.0.0:5000 wsgi