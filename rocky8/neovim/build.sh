#!/bin/bash

builder=$(buildah from rockylinux:8)

version="${1}"
echo "Building neovim version $version"

echo "Installing dependencies and setting up environment"

buildah run $builder -- bash -c \
	"dnf install -y 'dnf-command(config-manager)'"

buildah run $builder -- bash -c \
	"dnf config-manager --set-enabled powertools"

buildah run $builder -- bash -c \
	"dnf install -y epel-release"

buildah run $builder -- bash -c \
	"dnf install -y \
		cmake3 \
		git \
		gcc-toolset-10-gcc \
		gcc-toolset-10-gcc-c++ \
		desktop-file-utils \
		fdupes \
		gettext \
		gperf \
		ninja-build \
		unzip \
		autoconf \
		automake \
		make \
		pkgconfig \
		curl \
		jemalloc-devel \
		wget \
		luajit-devel \
		msgpack-devel \
		libtermkey-devel \
		libuv-devel \
		luajit2.1-luv \
		unibilium-devel \
		rpmdevtools"

buildah run $builder -- bash -c \
	"rpmdev-setuptree &&
	wget https://github.com/neovim/neovim/archive/refs/tags/v$version.tar.gz -P ~/rpmbuild/SOURCES"

echo "Copying specs into build container"
buildah copy $builder ./neovim.spec '/root/rpmbuild/SPECS/'
buildah copy $builder ./sysinit.vim ./neovim-lua-bit32.patch ./spec-template '/root/rpmbuild/SOURCES/'

echo "Bulding neovim RPM"
buildah run $builder -- bash -c \
	"QA_SKIP_BUILD_ROOT=1 rpmbuild -bs ~/rpmbuild/SPECS/neovim.spec --with jemalloc --with luajit &&
	 QA_SKIP_BUILD_ROOT=1 rpmbuild -bb ~/rpmbuild/SPECS/neovim.spec --with jemalloc --with luajit"

rm -rf build
mkdir -p build

mnt=$(buildah mount $builder)
cp -r $mnt/root/rpmbuild/RPMS/x86_64/* $mnt/root/rpmbuild/SRPMS/* build/
buildah umount $builder

buildah rm $builder
