## How to build the DB image
cd db_files
docker build -t vulns-mysql .
cd ..
docker-compose up --build --force-recreate

### Command to connect from the container
mysql -h 127.0.0.1 -P 3306 -u root -p


