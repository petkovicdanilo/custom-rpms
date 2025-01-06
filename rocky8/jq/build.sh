#!/bin/bash

builder=$(buildah from rockylinux:8)

version="${1}"
echo "Building jq version $version"

echo "Installing dependencies and setting up environment"

buildah run $builder -- bash -c \
	"dnf install -y 'dnf-command(config-manager)'"

buildah run $builder -- bash -c \
	"dnf config-manager --set-enabled powertools"

buildah run $builder -- bash -c \
	"dnf install -y \
		gcc \
		flex \
		bison \
		chrpath \
		oniguruma-devel \
		make \
		valgrind \
		autoconf \
		automake \
		libtool \
		wget \
		rpmdevtools"

buildah run $builder -- bash -c \
	"rpmdev-setuptree &&
	wget https://github.com/jqlang/jq/archive/refs/tags/jq-$version.tar.gz -P /root/rpmbuild/SOURCES"

buildah copy $builder ./jq.spec '/root/rpmbuild/SPECS/'
buildah copy $builder ./fix-version-output.patch '/root/rpmbuild/SOURCES/'

echo "Bulding jq RPM"
buildah run $builder -- bash -c \
	"rpmbuild -bs /root/rpmbuild/SPECS/jq.spec &&
	rpmbuild -bb /root/rpmbuild/SPECS/jq.spec"

rm -rf build
mkdir -p build

mnt=$(buildah mount $builder)
cp -r $mnt/root/rpmbuild/RPMS/x86_64/* $mnt/root/rpmbuild/SRPMS/* build/
buildah umount $builder

buildah rm $builder
