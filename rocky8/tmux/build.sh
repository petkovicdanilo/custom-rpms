#!/bin/bash

builder=$(buildah from rockylinux:8)

version="${1}"
echo "Building tmux version $version"

echo "Installing dependencies and setting up environment"

buildah run $builder -- bash -c \
	"dnf install -y 'dnf-command(config-manager)'"

buildah run $builder -- bash -c \
	"dnf config-manager --set-enabled powertools"

buildah run $builder -- bash -c \
	"dnf install -y \
		gcc \
		libevent-devel \
		ncurses-devel \
		wget \
		automake \
		make \
		bison \
		byacc \
		libutempter-devel \
		systemd-devel \
		rpmdevtools"

buildah run $builder -- bash -c \
	"rpmdev-setuptree &&
	wget https://github.com/tmux/tmux/archive/refs/tags/$version.tar.gz -P /root/rpmbuild/SOURCES"

buildah copy $builder ./tmux.spec '/root/rpmbuild/SPECS/'
buildah copy $builder ./bash_completion_tmux.sh '/root/rpmbuild/SOURCES/'
buildah copy $builder ./tmux@.service '/root/rpmbuild/SOURCES/'
buildah copy $builder ./systemd.patch '/root/rpmbuild/SOURCES/'

echo "Bulding tmux RPM"
buildah run $builder -- bash -c \
	"rpmbuild -bs /root/rpmbuild/SPECS/tmux.spec &&
	rpmbuild -bb /root/rpmbuild/SPECS/tmux.spec"

rm -rf build
mkdir -p build

mnt=$(buildah mount $builder)
cp -r $mnt/root/rpmbuild/RPMS/x86_64/* $mnt/root/rpmbuild/SRPMS/* build/
buildah umount $builder

buildah rm $builder
