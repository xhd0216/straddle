# straddle
make install

make test

python straddle -h

# also supports bazel
in /straddle

bazel build //...
bazel test //...
bazel clean


known issues:

1. marketwatch.com won't allow tlsv1 connection. if openssl version <= 0.9.8, please upgrade openssl to latest.
