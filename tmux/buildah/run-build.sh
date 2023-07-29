#!/bin/bash

version=${1:-"3.3a"}

buildah unshare ./build.sh "${version}"

