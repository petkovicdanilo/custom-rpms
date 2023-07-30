#!/bin/bash

version=${1:-"3.27.1"}

buildah unshare ./build.sh "${version}"

