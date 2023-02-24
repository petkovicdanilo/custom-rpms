#!/bin/bash
tag="2023-02-20"

buildah bud -t centos7-rust-analyzer:$tag --build-arg tag=$tag .

rm -rf build
mkdir build

id=$(podman create centos7-rust-analyzer:$tag)
podman cp $id:/rust-analyzer build/
podman rm -v $id

