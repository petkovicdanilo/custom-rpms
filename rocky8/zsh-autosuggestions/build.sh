#!/bin/bash

builder=$(buildah from rockylinux:8)

version="${1}"
echo "Building zsh-autosuggestions version $version"

echo "Installing dependencies and setting up environment"

buildah run $builder -- bash -c \
	"dnf install -y \
		make \
		zsh \
		wget \
		rpmdevtools"

echo "Downloading zsh-autosuggestions source"

buildah run $builder -- bash -c \
	"rpmdev-setuptree &&
	wget https://github.com/zsh-users/zsh-autosuggestions/archive/refs/tags/v$version.tar.gz -P /root/rpmbuild/SOURCES"

buildah copy $builder ./zsh-autosuggestions.spec '/root/rpmbuild/SPECS/'

echo "Bulding zsh-autosuggestions RPM"
buildah run $builder -- bash -c \
	"rpmbuild -bs /root/rpmbuild/SPECS/zsh-autosuggestions.spec &&
	rpmbuild -bb /root/rpmbuild/SPECS/zsh-autosuggestions.spec"

rm -rf build
mkdir -p build

mnt=$(buildah mount $builder)
cp -r $mnt/root/rpmbuild/RPMS/noarch/* $mnt/root/rpmbuild/SRPMS/* build/
buildah umount $builder

buildah rm $builder
