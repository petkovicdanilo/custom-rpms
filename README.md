# Centos 7 packages

This repo contains build scripts for some of the programs I use in Centos 7. 
They are in newer versions than those available in official Centos 7 repos.
In the [Release](https://github.com/petkovicdanilo/centos7-packages/releases) 
section you can find already built artifacts (mostly RPMs) for all packages.

## Build requirements

Build of all the packages is completely containerized.
That means that you can use any platform that supports
`buildah` since that is the tool used to set up
containerized environment and build the package inside it.

To be able to build RPMs from source you will need:
- `make`
- `buildah`

## Building

### Build all packages

To build all packages run

```bash
make
```

### Build one package

To build one package, run `make` with its name.

For example for `neovim`
```bash
make neovim
```

Alternatively, you can look for build instructions for each
package inside of its directory.

## Installation

You can either build packages for youself or download 
already built packages from [Release](https://github.com/petkovicdanilo/centos7-packages/releases) 

In case program is packaged as RPM you can install it using `yum`

```bash
yum install <package-name>.rpm
```

Note: Use binary `.rpm` here, not `.src.rpm`.

You can find installation instructions inside every package separately.
