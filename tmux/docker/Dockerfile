FROM centos:7 AS builder

RUN yum install -y \
	gcc \
	libevent-devel \
	ncurses-devel \
	git \
	automake \
	make \
	bison

RUN git clone https://github.com/tmux/tmux /usr/local/src/tmux

COPY ./tmux-build.sh /
RUN /tmux-build.sh

FROM centos:7

RUN mkdir /tmux
COPY --from=builder /build /tmux
