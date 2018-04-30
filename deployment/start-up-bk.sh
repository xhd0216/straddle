#!/bin/bash

# TODO: docker pull mysql

while [ "$1" != "" ]; do
    case $1 in
        --subnet )           shift
                             subnet_str=$1
                             ;;
        -h | --help )        usage
                             exit
                             ;;
        * )                  usage
                             exit 1
    esac
    shift
done

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

# TODO: check if pwgen exists
# create password
password=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 15; echo '')

ipaddress=172.28.88.$(shuf -i 33-233 -n 1)

mynetwork_name=test_network123

subnet_str=${osubnet_str:-"172.28.0.0/16"}
# create own network
mynetwork=$(sudo docker network ls -f name=$mynetwork_name -q)

if [[ $mynetwork ]]; then
  echo "network is already created"
else
  sudo docker network create --subnet=subnet_str $mynetwork_name
  if [ "$?" != "0" ]; then 
    echo "failed to create network" 1>&2
    exit 1
fi
  
# bring up container
container=$(sudo docker run --restart unless-stopped --name=test-mysql -dit --net $mynetwork_name --ip="$ipaddress" --env="MYSQL_ROOT_PASSWORD=$password" mysql)
echo "container is up $container"

# create database
sed "s/IPADDR/$ipaddress/g;s/PASSWORD/$password/g" $SCRIPTPATH/cnf-template.cnf > $SCRIPTPATH/test-options.cnf
echo "created cnf file"

echo "sleeping for 60 seconds, wait for mysql to start"
sleep 60

mysql --defaults-extra-file=./test-options.cnf -e "create database options;"
echo "create database"

echo "database=options" >> $SCRIPTPATH/test-options.cnf

mysql --defaults-extra-file=./test-options.cnf -e "source ./create_option_table.sql"
