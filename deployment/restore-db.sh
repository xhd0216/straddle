#!/bin/bash

# TODO: parameterize config file and sql file

read -r thost tport tuser tpass tdb <<< $(awk -F"=" '{print $2}' test-options.cnf)

# Restore
cat backup.sql | docker exec -i test-mysql /usr/bin/mysql -u root --password=root options
