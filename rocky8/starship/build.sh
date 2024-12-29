#!/bin/bash

builder=$(buildah from rockylinux:8)

version="${1}"
echo "Building starship version $version"

echo "Installing dependencies and setting up environment"

buildah run $builder -- bash -c \
	"dnf install -y \
		gcc \
		gcc-c++ \
		cmake \
		curl \
		wget \
		rpmdevtools"

echo "Installing Rust"

buildah run $builder -- bash -c \
	"curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs > /tmp/rustup.sh &&
	sh /tmp/rustup.sh -y --profile=minimal"

echo "Downloading starship source"

buildah run $builder -- bash -c \
	"rpmdev-setuptree &&
	wget https://github.com/starship/starship/archive/refs/tags/v$version.tar.gz -P /root/rpmbuild/SOURCES"

buildah copy $builder ./starship.spec '/root/rpmbuild/SPECS/'

echo "Bulding starship RPM"
buildah run $builder -- bash -c \
	"rpmbuild -bs /root/rpmbuild/SPECS/starship.spec &&
	rpmbuild -bb /root/rpmbuild/SPECS/starship.spec"

rm -rf build
mkdir -p build

mnt=$(buildah mount $builder)
cp -r $mnt/root/rpmbuild/RPMS/x86_64/* $mnt/root/rpmbuild/SRPMS/* build/
buildah umount $builder

buildah rm $builder
