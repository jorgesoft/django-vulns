# Use the official MySQL image as the base
FROM mysql:8.0

# Add your custom SQL schema file
ADD schema.sql /docker-entrypoint-initdb.d
ADD z_default_data.sql /docker-entrypoint-initdb.d

# Optional: Set environment variables
#ENV MYSQL_DATABASE=mydatabase
#ENV MYSQL_ROOT_PASSWORD=mysupersecretpassword
# Add any other environment variables you need
