# straddle #

## make ##
make install

make test

python straddle -h


## bazel ##
in /straddle

bazel build //...
bazel test //...
bazel clean

## docker ##
sudo docker build .


## known issues: ##

1. marketwatch.com won't allow tlsv1 connection. if openssl version <= 0.9.8, please upgrade openssl to latest. or, use docker
