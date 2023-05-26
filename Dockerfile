# start from an official image
FROM python:3.8

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# install our two dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install -r /app/requirements.txt

# copy our project code
COPY . /app/