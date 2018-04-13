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
```bash
sudo docker build .
sudo docker images
sudo docker run -dit --name straddle-image [image ID]
sudo exec -it straddle-image /bin/bash
```

## known issues: ##

1. marketwatch.com won't allow tlsv1 connection. if openssl version <= 0.9.8, please upgrade openssl to latest. or, use docker
