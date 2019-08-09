# Pull base image
FROM python:3.7-slim


# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Set working directory
WORKDIR /code


# Copy project & install dependencies
COPY . /code/
RUN pip install -r api/requirements.txt