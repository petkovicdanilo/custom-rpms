#!/bin/bash

builder=$(buildah from rockylinux:8)

version="${1}"
echo "Building zsh-vi-mode version $version"

echo "Installing dependencies and setting up environment"

buildah run $builder -- bash -c \
	"dnf install -y \
		zsh \
		wget \
		rpmdevtools"

echo "Downloading zsh-vi-mode source"

buildah run $builder -- bash -c \
	"rpmdev-setuptree &&
	wget https://github.com/jeffreytse/zsh-vi-mode/archive/refs/tags/v$version.tar.gz -P /root/rpmbuild/SOURCES"

buildah copy $builder ./zsh-vi-mode.spec '/root/rpmbuild/SPECS/'

echo "Bulding zsh-vi-mode RPM"
buildah run $builder -- bash -c \
	"rpmbuild -bs /root/rpmbuild/SPECS/zsh-vi-mode.spec &&
	rpmbuild -bb /root/rpmbuild/SPECS/zsh-vi-mode.spec"

rm -rf build
mkdir -p build

mnt=$(buildah mount $builder)
cp -r $mnt/root/rpmbuild/RPMS/noarch/* $mnt/root/rpmbuild/SRPMS/* build/
buildah umount $builder

buildah rm $builder
