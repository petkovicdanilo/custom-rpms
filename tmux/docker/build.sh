#!/bin/bash
docker build -t centos7-tmux .

mkdir -p build
rm -rf build/*

id=$(docker create centos7-tmux)
docker cp $id:/tmux build/
docker rm -v $id

