#!/bin/bash

builder=$(buildah from centos:7)

version="${1}"
echo "Building cmake version $version"

echo "Installing dependencies and setting up environment"
buildah run $builder -- bash -c \
	"yum install -y \
		openssl-devel \
		autoconf \
		automake \
		make \
		wget \
		centos-release-scl"

buildah run $builder -- bash -c "yum install -y devtoolset-10"

echo "Building"
buildah run $builder -- bash -c \
	"mkdir -p /usr/local/src/cmake && pushd /usr/local/src/cmake && 
	wget https://github.com/Kitware/CMake/archive/refs/tags/v${version}.tar.gz && tar xzf v${version}.tar.gz &&
	source /opt/rh/devtoolset-10/enable && 
	cd "CMake-${version}" && mkdir -p /cmake && 
	./bootstrap --prefix=/cmake && make && make install && popd"

rm -rf build/$version
mkdir -p build/$version

mnt=$(buildah mount $builder)
cp -r $mnt/cmake build/$version
buildah umount $builder

buildah rm $builder
