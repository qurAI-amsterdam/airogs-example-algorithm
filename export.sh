#!/usr/bin/env bash

./build.sh

docker save airogs_algorithm | gzip -c > airogs_algorithm.tar.gz
