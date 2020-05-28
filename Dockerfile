FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code && \
    apt-get install -y ruby
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/