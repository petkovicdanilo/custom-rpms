#!/bin/bash
cd /usr/local/src/neovim
scl enable devtoolset-10 bash
export CXX=/opt/rh/devtoolset-10/root/usr/bin/g++
git checkout stable
make CMAKE_BUILD_TYPE=Release CMAKE_INSTALL_PREFIX=/build install
