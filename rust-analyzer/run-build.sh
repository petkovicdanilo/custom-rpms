#!/bin/bash

tag=${1:-"master"}

buildah unshare ./build.sh "${tag}"

