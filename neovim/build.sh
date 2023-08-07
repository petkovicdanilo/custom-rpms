#!/bin/bash

builder=$(buildah from centos:7)

version="${1}"
echo "Building neovim version $version"

echo "Installing dependencies and setting up environment"

buildah run $builder -- bash -c \
	"yum install -y epel-release centos-release-scl"
buildah run $builder -- bash -c \
	"yum install -y \
		cmake3 \
		git \
		devtoolset-10-gcc \
		devtoolset-10-gcc-c++ \
		desktop-file-utils \
		fdupes \
		gettext \
		gperf \
		ninja-build \
		unzip \
		autoconf \
		automake \
		make \
		pkconfig \
		curl \
		jemalloc-devel \
		wget \
		rpmdevtools"

buildah run $builder -- bash -c \
	"rpmdev-setuptree &&
	wget https://github.com/neovim/neovim/archive/refs/tags/v$version.tar.gz -P ~/rpmbuild/SOURCES"

echo "Copying specs into build container"
buildah copy $builder ./neovim.spec '/root/rpmbuild/SPECS/'
buildah copy $builder ./sysinit.vim ./spec-template ./neovim-lua-bit32.patch '/root/rpmbuild/SOURCES/'

echo "Bulding neovim RPM"
buildah run $builder -- bash -c \
	"QA_SKIP_BUILD_ROOT=1 rpmbuild -bs ~/rpmbuild/SPECS/neovim.spec --with jemalloc &&
	 QA_SKIP_BUILD_ROOT=1 rpmbuild -bb ~/rpmbuild/SPECS/neovim.spec --with jemalloc"

rm -rf build
mkdir -p build

mnt=$(buildah mount $builder)
cp -r $mnt/root/rpmbuild/RPMS/x86_64/* $mnt/root/rpmbuild/SRPMS/* build/
buildah umount $builder

buildah rm $builder
