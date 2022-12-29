#!/bin/bash
docker build -t centos7-neovim .

mkdir -p build
rm -rf build/*

id=$(docker create centos7-neovim)
docker cp $id:/nvim build/
docker rm -v $id

