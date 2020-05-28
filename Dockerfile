FROM python:3
ENV PYTHONUNBUFFERED 1
RUN sudo apt install ruby
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/