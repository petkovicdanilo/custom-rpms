#!/bin/bash

builder=$(buildah from rockylinux:8)

version="${1}"
echo "Building eza version $version"

echo "Installing dependencies and setting up environment"

buildah run $builder -- bash -c \
	"dnf install -y 'dnf-command(config-manager)'"

buildah run $builder -- bash -c \
	"dnf config-manager --set-enabled powertools"

buildah run $builder -- bash -c \
	"dnf install -y \
		gcc \
		curl \
		pandoc \
		wget \
		rpmdevtools"

echo "Installing Rust"

buildah run $builder -- bash -c \
	"curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs > /tmp/rustup.sh &&
	sh /tmp/rustup.sh -y --profile=minimal"

echo "Installing Rust depencencies"

JUST_VERSION=1.38.0
buildah run $builder -- bash -c \
	"source ~/.cargo/env && cargo install just@$JUST_VERSION"

echo "Downloading eza source"

buildah run $builder -- bash -c \
	"rpmdev-setuptree &&
	wget https://github.com/eza-community/eza/archive/refs/tags/v$version.tar.gz -P /root/rpmbuild/SOURCES"

buildah copy $builder ./eza.spec '/root/rpmbuild/SPECS/'

echo "Bulding eza RPM"
buildah run $builder -- bash -c \
	"rpmbuild -bs /root/rpmbuild/SPECS/eza.spec &&
	rpmbuild -bb /root/rpmbuild/SPECS/eza.spec"

rm -rf build
mkdir -p build

mnt=$(buildah mount $builder)
cp -r $mnt/root/rpmbuild/RPMS/x86_64/* $mnt/root/rpmbuild/SRPMS/* build/
buildah umount $builder

buildah rm $builder
