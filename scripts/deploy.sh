#!/bin/bash

if [ "$1" == "-prod" ]; then
    cd django-vulns
    git pull
fi

docker compose down -v
cd db_files
docker build -t vulns-mysql .
cd ..
docker-compose up --build --force-recreate
