FROM centos:7 AS builder

ARG tag=master

RUN yum groupinstall -y "Development tools" && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \ 
    yum install -y epel-release && yum install -y nodejs npm

RUN git clone https://github.com/rust-lang/rust-analyzer.git && cd rust-analyzer && git checkout $tag

COPY ./rust-analyzer-build.sh /
RUN /rust-analyzer-build.sh

FROM centos:7

RUN mkdir /rust-analyzer
COPY --from=builder /rust-analyzer/target/release/rust-analyzer /rust-analyzer
COPY --from=builder /rust-analyzer/editors/code/rust-analyzer.vsix /rust-analyzer
