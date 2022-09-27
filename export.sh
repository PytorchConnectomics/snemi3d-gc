#!/usr/bin/env bash

./build.sh

docker save snemi3d | gzip -c > snemi3d.tar.gz
