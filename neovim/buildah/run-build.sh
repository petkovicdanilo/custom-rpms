#!/bin/bash

version=${1:-"stable"}

buildah unshare ./build.sh "${version}"

