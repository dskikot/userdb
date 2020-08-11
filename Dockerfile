# pull official base image
FROM python:3.8

# set work directory
#WORKDIR /home/userdb

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

# install dependencies
RUN pip install --upgrade pip setuptools
COPY requirements.txt /code/
RUN pip install -r requirements.txt
# copy project
COPY . /code/
