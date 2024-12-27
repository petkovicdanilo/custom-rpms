#!/bin/bash

builder=$(buildah from centos:7)

version="${1}"
echo "Building tmux version $version"

echo "Installing dependencies and setting up environment"
buildah run $builder -- bash -c \
	"yum install -y \
		gcc \
		libevent-devel \
		ncurses-devel \
		wget \
		automake \
		make \
		bison \
		rpmdevtools"

buildah run $builder -- bash -c \
	"rpmdev-setuptree &&
	wget https://github.com/tmux/tmux/archive/refs/tags/$version.tar.gz -P ~/rpmbuild/SOURCES"

buildah copy $builder ./tmux.spec '/root/rpmbuild/SPECS/'
buildah copy $builder ./bash_completion_tmux.sh '/root/rpmbuild/SOURCES/'

echo "Bulding tmux RPM"
buildah run $builder -- bash -c \
	"rpmbuild -bs ~/rpmbuild/SPECS/tmux.spec &&
	rpmbuild -bb ~/rpmbuild/SPECS/tmux.spec"

rm -rf build
mkdir -p build

mnt=$(buildah mount $builder)
cp -r $mnt/root/rpmbuild/RPMS/x86_64/* $mnt/root/rpmbuild/SRPMS/* build/
buildah umount $builder

buildah rm $builder
