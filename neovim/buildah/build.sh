#!/bin/bash

builder=$(buildah from centos:7)

version="${1}"
echo "Building neovim version $version"

echo "Installing dependencies and setting up environment"
buildah run $builder -- bash -c \
	"yum install -y \
		ninja-build \
		libtool \
		autoconf \
		automake \
		make \
		pkgconfig \
		unzip \
		patch \
		gettext \
		curl \
		centos-release-scl \
		https://packages.endpointdev.com/rhel/7/os/x86_64/endpoint-repo.x86_64.rpm"

buildah run $builder -- bash -c "yum install -y devtoolset-10 git"

buildah run $builder -- bash -c \
	"mkdir -p /usr/local/src/cmake && pushd /usr/local/src/cmake &&
	curl -LO https://github.com/Kitware/CMake/releases/download/v3.22.2/cmake-3.22.2-linux-x86_64.tar.gz &&
	tar -xzf cmake-3.22.2-linux-x86_64.tar.gz && 
	cp -r cmake-3.22.2-linux-x86_64/* /usr/local &&
	popd"

echo "Cloning neovim repo"
buildah run $builder -- bash -c "git clone https://github.com/neovim/neovim /usr/local/src/neovim"

echo "Building"
buildah run $builder -- bash -c \
	"pushd /usr/local/src/neovim &&
	source /opt/rh/devtoolset-10/enable &&
	git checkout $version &&
	make CMAKE_BUILD_TYPE=Release CMAKE_INSTALL_PREFIX=/nvim install"

rm -rf build/$version
mkdir -p build/$version

mnt=$(buildah mount $builder)
cp -r $mnt/nvim build/$version
buildah umount $builder

buildah rm $builder
