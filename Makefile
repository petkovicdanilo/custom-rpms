.PHONY: all
all: neovim rust-analyzer tmux

.PHONY: neovim
neovim:
	cd neovim && $(MAKE) && cd -
.PHONY: rust-analyzer
rust-analyzer:
	cd rust-analyzer && $(MAKE) && cd -
.PHONY: tmux
tmux:
	cd tmux && $(MAKE) && cd -
