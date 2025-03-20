FROM mysql:5.7
ENV MYSQL_DATABASE=anime
ENV MYSQL_USER=julien
ENV MYSQL_PASSWORD=pass
ENV MYSQL_ROOT_PASSWORD=pass
COPY script.sql /docker-entrypoint-initdb.d
EXPOSE 3306
