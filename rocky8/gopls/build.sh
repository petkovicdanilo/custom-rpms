#!/bin/bash

builder=$(buildah from rockylinux:8)

version="${1}"
echo "Building gopls version $version"

echo "Installing dependencies and setting up environment"

buildah run $builder -- bash -c \
	"dnf install -y \
		gcc \
		make \
		wget \
		rpmdevtools"

echo "Installing Golang"

GO_VERSION=1.23.4

buildah run $builder -- bash -c \
	"wget https://go.dev/dl/go$GO_VERSION.linux-amd64.tar.gz -P /tmp && \
	rm -rf /usr/local/go && \
	tar -C /usr/local -xzf /tmp/go$GO_VERSION.linux-amd64.tar.gz"

echo "Downloading gopls source"

buildah run $builder -- bash -c \
	"rpmdev-setuptree &&
	wget https://github.com/golang/tools/archive/refs/tags/gopls/v$version.tar.gz -P /root/rpmbuild/SOURCES"

buildah copy $builder ./gopls.spec '/root/rpmbuild/SPECS/'

echo "Bulding gopls RPM"
buildah run $builder -- bash -c \
	"rpmbuild -bs /root/rpmbuild/SPECS/gopls.spec &&
	rpmbuild -bb /root/rpmbuild/SPECS/gopls.spec"

rm -rf build
mkdir -p build

mnt=$(buildah mount $builder)
cp -r $mnt/root/rpmbuild/RPMS/x86_64/* $mnt/root/rpmbuild/SRPMS/* build/
buildah umount $builder

buildah rm $builder
