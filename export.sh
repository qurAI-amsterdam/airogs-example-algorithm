#!/usr/bin/env bash

./build.sh

docker save airogs_algorithm | xz -c > airogs_algorithm.tar.xz
