#!/bin/bash

builder=$(buildah from centos:7)

version="${1}"
echo "Building tmux version $version"

echo "Installing dependencies and setting up environment"
buildah run $builder -- bash -c \
	"yum install -y \
		gcc \
		libevent-devel \
		ncurses-devel \
		git \
		automake \
		make \
		bison"

buildah run $builder -- bash -c \
	"git clone https://github.com/tmux/tmux /usr/local/src/tmux &&
	cd /usr/local/src/tmux && git checkout 3.3a &&
	
	mkdir /build && sh autogen.sh && ./configure --prefix=/tmux && 
	make && make install"

rm -rf build/$version
mkdir -p build/$version

mnt=$(buildah mount $builder)
cp -r $mnt/tmux build/$version
buildah umount $builder

buildah rm $builder
