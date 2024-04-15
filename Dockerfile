# Using official Python installed in my pc
FROM python:3.10.12

# Setting environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Setting work directory
WORKDIR /app

# Updating and installing needed dependencies
RUN apt-get update \
  && apt-get install -y build-essential default-libmysqlclient-dev \
  # Cleaning up to keep the docker image light
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install my dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the wait-for-it.sh script to wait until the db container is ready to start Django server
COPY scripts/wait-for-it.sh scripts/wait-for-it.sh
RUN chmod +x scripts/wait-for-it.sh

# Copying project
COPY . /app/
