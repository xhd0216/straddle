#!/bin/bash

# TODO: parameterize config file and sql file

# Restore
cat backup.sql | mysql --defaults-extra-file=test-options.cnf
