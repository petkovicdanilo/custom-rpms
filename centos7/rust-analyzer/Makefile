version ?= "2024-02-26"
.PHONY: build
build:
	buildah unshare ./build.sh $(version)

package: build
	gzip --keep build/rust-analyzer
