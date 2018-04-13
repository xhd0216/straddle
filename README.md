# straddle #

## make ##
```bash
make install
make test
```

## bazel ##
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

  * [marketwatch](https://marketwatch.com) won't allow tlsv1 connection. if openssl version <= 0.9.8, upgrade `openssl` to >= 1.0.1. or, use docker.
