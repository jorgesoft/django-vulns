# Using the official MySQL image as the base
FROM mysql:8.0

# Adding custom SQL schema file
ADD schema.sql /docker-entrypoint-initdb.d
ADD z_default_data.sql /docker-entrypoint-initdb.d

# Setting password and db settings
#ENV MYSQL_DATABASE=mydatabase
#ENV MYSQL_ROOT_PASSWORD=mysupersecretpassword
