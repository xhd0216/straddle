#!/bin/bash

read -r thost tport tuser tpass tdb <<< $(awk -F"=" '{print $2}' test-options.cnf)


# Backup
/usr/bin/mysqldump --host="$thost" --user="$tuser" --port="$tport" --password="$tpass" $tdb 1>backup.sql 2>/dev/null

# Restore
#cat backup.sql | docker exec -i CONTAINER /usr/bin/mysql -u root --password=root DATABASE
