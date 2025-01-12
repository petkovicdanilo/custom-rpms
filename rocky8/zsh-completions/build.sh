#!/bin/bash

builder=$(buildah from rockylinux:8)

version="${1}"
echo "Building zsh-completions version $version"

echo "Installing dependencies and setting up environment"

buildah run $builder -- bash -c \
	"dnf install -y \
		zsh \
		wget \
		rpmdevtools"

echo "Downloading zsh-completions source"

buildah run $builder -- bash -c \
	"rpmdev-setuptree &&
	wget https://github.com/zsh-users/zsh-completions/archive/refs/tags/$version.tar.gz -P /root/rpmbuild/SOURCES"

buildah copy $builder ./zsh-completions.spec '/root/rpmbuild/SPECS/'

echo "Bulding zsh-completions RPM"
buildah run $builder -- bash -c \
	"rpmbuild -bs /root/rpmbuild/SPECS/zsh-completions.spec &&
	rpmbuild -bb /root/rpmbuild/SPECS/zsh-completions.spec"

rm -rf build
mkdir -p build

mnt=$(buildah mount $builder)
cp -r $mnt/root/rpmbuild/RPMS/noarch/* $mnt/root/rpmbuild/SRPMS/* build/
buildah umount $builder

buildah rm $builder
