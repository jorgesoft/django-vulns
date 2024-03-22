# Use an official Python runtime as a parent image
FROM python:3.10.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install any needed system dependencies here
# First, update the list of packages
RUN apt-get update \
  # Then install the necessary packages
  # For example, here we install the build-essential and default-libmysqlclient-dev packages
  # build-essential is often needed for packages that require compilation
  # default-libmysqlclient-dev is required for the mysqlclient Python package
  && apt-get install -y build-essential default-libmysqlclient-dev \
  # Clean up to keep the docker image clean
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the wait-for-it.sh script
COPY wait-for-it.sh /wait-for-it.sh
# Make sure the script is executable
RUN chmod +x /wait-for-it.sh

# Copy project
COPY . /app/
