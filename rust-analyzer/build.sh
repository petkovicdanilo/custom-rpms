#!/bin/bash

builder=$(buildah from centos:7)

version="${1}"
echo "Building rust-analyzer version $version"

buildah run $builder -- bash -c \
    "yum groupinstall -y \"Development tools\" &&
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y &&
    yum install -y epel-release && yum install -y nodejs npm"

buildah run $builder -- bash -c \
    "git clone https://github.com/rust-lang/rust-analyzer.git && cd rust-analyzer && git checkout $tag"

buildah run $builder -- bash -c "cd /rust-analyzer && source ~/.bashrc && (cargo xtask install || :)"

rm -rf build/$tag
mkdir -p build/$tag

mnt=$(buildah mount $builder)
cp $mnt/rust-analyzer/target/release/rust-analyzer build/$tag
cp $mnt/rust-analyzer/editors/code/rust-analyzer.vsix build/$tag
buildah umount $builder

buildah rm $builder
