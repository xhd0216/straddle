# Deployments #

## deploy main docker ##
there are two docker images to deploy, choose either one:
```bash
docker build . # if not done before
docker images # find image id
docker run -dit --name main-docker --restart unless-stopped [image id]
```
To set up crontab job, modify `cron.ext` before building image.

Alternatively, there is another Docker file under `r/` folder. use the same docker command to run the container. Note that it does not support crontab job yet.

To access the docker container, do
```bash
docker exec -it main-docker /bin/bash
```

## deploy mysql server ##
```bash
./start-up.sh
```
It will create a file `test-options.cnf`, which will be used to connect to mysql server like
```bash
mysql --defualts-extra-file=./test-options.cnf
```
To enter the mysql server docker container, do
```bash
docker exec -it test-mysql /bin/bash
```
To backup and restore database (user, password and database can be found in `test-options.cnf`):
```bash
docker exec test-mysql /usr/bin/mysqldump -u root --password=PW DATABASE > backup.sql
cat backup.sql | docker exec -i test-mysql /usr/bin/mysql -u root --password=root DATABASE
```

## deploy httpd server ##
```bash
docker pull httpd # if not done yet
docker images # find image id
docker run -dit --name httpd --restart unless-stopped -p 80:80 [image id]
```
