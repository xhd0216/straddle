#!/bin/bash


# if container already exists
running=$(sudo docker ps -f "name=test-mysql" -q)
if [[ $running ]]; then 
  echo "container is already running $running";
  exit 0
else
  stopped=$(sudo docker ps -f "name=test-mysql" -qa)
  if [[ $stopped ]]; then
    echo "restart $stopped"
    sudo docker restart $stopped
    exit 0
  fi
fi

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
if [ ! -f $SCRIPTPATH/cnf-template.cnf ]; then
  echo "$SCRIPTPATH/cnf-template.cnf template file not found"
  exit 2
fi

# create password
password=$(pwgen 15 1)

# bring up container
container=$(sudo docker run --restart unless-stopped --name=test-mysql -dit --env="MYSQL_ROOT_PASSWORD=$password" mysql)
echo "container is up $container"

# get IP
ipaddress=$(sudo docker inspect $container | grep \"IPAddress\" | awk -F\" '{print $4}' | head -n 1)
echo "get IP $ipaddress"

# create database
sed "s/IPADDR/$ipaddress/g;s/PASSWORD/$password/g" $SCRIPTPATH/cnf-template.cnf > $SCRIPTPATH/test-options.cnf
echo "created cnf file"

echo "sleeping for 60 seconds, wait for mysql to start"
sleep 60

mysql --defaults-extra-file=./test-options.cnf -e "create database options;"
echo "create database"

echo "database=options" >> $SCRIPTPATH/test-options.cnf

mysql --defaults-extra-file=./test-options.cnf -e "source ./create_option_table.sql"
