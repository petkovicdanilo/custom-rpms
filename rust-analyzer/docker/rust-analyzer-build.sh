#!/bin/bash
source ~/.bashrc && cd /rust-analyzer

cargo xtask install || :

