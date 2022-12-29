mkdir -p /usr/local/src/cmake
cd /usr/local/src/cmake

curl -LO https://github.com/Kitware/CMake/releases/download/v3.22.2/cmake-3.22.2-linux-x86_64.tar.gz
tar -xzf cmake-3.22.2-linux-x86_64.tar.gz

cp -r cmake-3.22.2-linux-x86_64/* /usr/local
