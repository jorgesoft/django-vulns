cd db_files
docker build -t vulns-mysql .
cd ..
docker-compose up --build --force-recreate


mysql -h 127.0.0.1 -P 3306 -u root -p


