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
in `docker/`:

  * start mysql database in docker:
```bash
    bash ./start-up.sh
```
  * start docker container:
```bash
    sudo docker build .
    sudo docker images # find image ID
    sudo docker run -dit --name straddle-image [image ID]
    sudo docker exec -it straddle-image /bin/bash
```

## known issues: ##

  * [marketwatch](https://www.marketwatch.com) won't allow tlsv1 connection. if openssl version <= 0.9.8, upgrade `openssl` to >= 1.0.1. or, use docker.
