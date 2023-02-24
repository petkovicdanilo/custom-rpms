#!/bin/bash
tag="2023-02-20"

docker build -t centos7-rust-analyzer:$tag --build-arg tag=$tag .

rm -rf build
mkdir build

id=$(docker create centos7-rust-analyzer:$tag)
docker cp $id:/rust-analyzer build/
docker rm -v $id

