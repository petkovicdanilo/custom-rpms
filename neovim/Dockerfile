FROM centos:7 AS builder

RUN yum install -y \
	ninja-build \
	libtool \
	autoconf \
	automake \
	make \
	pkgconfig \
	unzip \
	patch \
	gettext \
	curl \
	centos-release-scl \
	https://packages.endpointdev.com/rhel/7/os/x86_64/endpoint-repo.x86_64.rpm

RUN yum install -y devtoolset-10 git

RUN mkdir /scripts /build

COPY ./install-cmake3.sh /scripts
RUN /scripts/install-cmake3.sh

RUN git clone https://github.com/neovim/neovim /usr/local/src/neovim

COPY ./neovim-build.sh /scripts
RUN /scripts/neovim-build.sh

FROM centos:7

RUN mkdir /nvim
COPY --from=builder /build /nvim
