#!/bin/bash

version=${1:-"0.9.1"}

buildah unshare ./build.sh "${version}"

