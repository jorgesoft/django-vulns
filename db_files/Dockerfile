# Using the official MySQL image as the base
FROM mysql:8.0

# Adding custom SQL schema file
COPY ./sql_files/ /docker-entrypoint-initdb.d/

# Setting password and db settings
#ENV MYSQL_DATABASE=mydatabase
#ENV MYSQL_ROOT_PASSWORD=mysupersecretpassword
