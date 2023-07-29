#!/bin/bash
cd /usr/local/src/neovim
source /opt/rh/devtoolset-10/enable
git checkout stable
make CMAKE_BUILD_TYPE=Release CMAKE_INSTALL_PREFIX=/nvim install
