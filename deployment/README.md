# Deployments #

## deploy mysql server ##
```bash
./start-up.sh
```
it will create a file `test-options.cnf`, which will be used to connect to mysql server like
```bash
mysql --defualts-extra-file=./test-options.cnf
```

## deploy httpd server ##
```bash
docker pull httpd # if not done yet
docker images # find image id
docker run -dit --name httpd --restart unless-stopped -p 80:80 [image id]
```
