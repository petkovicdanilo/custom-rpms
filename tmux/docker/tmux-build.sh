#!/bin/bash
cd /usr/local/src/tmux

git checkout 3.3a

mkdir /build
sh autogen.sh

./configure --prefix=/build && make
make install
