# straddle #

## make ##
```bash
make install
make test
```

## bazel ##
in /straddle
```bash
bazel build //...
bazel test //...
bazel clean
```

## docker ##
```bash
sudo docker build .
sudo docker images
sudo docker run -dit --name straddle-image [image ID]
sudo docker exec -it straddle-image /bin/bash
```

## known issues: ##

1. [marketwatch](https://markeywatch.com) won't allow tlsv1 connection. if openssl version <= 0.9.8, upgrade `openssl` to >= 1.0.1. or, use docker.
