# Custom RPMs

This repo contains build scripts for newer versions of some programs that I use
that are newer versions compared to those available in the original repos.

Per distro packages can be found in separate directories:
- [Centos 7](centos7)
- [Rocky 8](rocky8)

In the [Release](https://github.com/petkovicdanilo/custom-rpms/releases) 
section you can find already built artifacts (mostly RPMs) for all packages.

## Build requirements

Build of all the packages is completely containerized.
That means that you can use any platform that supports
`buildah` since that is the tool used to set up
containerized environment and build the package inside it.

To be able to build RPMs from source you will need:
- `make`
- `buildah`
