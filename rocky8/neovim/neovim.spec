%define  debug_package %{nil}

%bcond_with jemalloc

%bcond_without luajit

Name:           neovim
Version:        0.11.0
Release:        1%{?dist}

License:        Apache-2.0 AND Vim
Summary:        Vim-fork focused on extensibility and agility
Url:            https://neovim.io

Source0:        https://github.com/neovim/neovim/archive/refs/tags/v%{version}.tar.gz
Source1:        sysinit.vim
Source2:        spec-template

Patch1000:      neovim-lua-bit32.patch

BuildRequires:  cmake3
BuildRequires:  gcc-toolset-10-gcc
BuildRequires:  gcc-toolset-10-gcc-c++
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes
BuildRequires:  gettext
BuildRequires:  gperf

%if %{with luajit}
BuildRequires:  luajit-devel
# TODO min version for luajit2.1-luv
Requires:       luajit2.1-luv
%else
BuildRequires:  compat-lua
BuildRequires:  compat-lua-devel
BuildRequires:  lua5.1-bit32
# TODO min version
Requires:       lua5.1-luv
%endif
	
# Requires:       lua5.1-lpeg >= 1.1.0
# BuildRequires:  lua5.1-lpeg >= 1.1.0
# BuildRequires:  lua5.1-mpack >= 1.0.11

%if %{with jemalloc}
BuildRequires:  jemalloc-devel
%endif

BuildRequires:  msgpack-devel >= 3.1.0
BuildRequires:  pkgconfig(termkey)
BuildRequires:  pkgconfig(unibilium)
BuildRequires:  libtermkey-devel
Requires:       libtermkey
BuildRequires:  libuv-devel
Requires:       libuv
BuildRequires:  unibilium-devel
Requires:       unibilium

Recommends:     tree-sitter-cli
Suggests:       (python2-neovim if python2)
Suggests:       (python3-neovim if python3)
# XSel provides access to the system clipboard
Recommends:     xsel
Recommends:     wl-clipboard
Recommends:     ripgrep
Recommends:     inotify-tools

%description
Neovim is a refactor - and sometimes redactor - in the tradition of
Vim, which itself derives from Stevie. It is not a rewrite, but a
continuation and extension of Vim. Many rewrites, clones, emulators
and imitators exist; some are very clever, but none are Vim. Neovim
strives to be a superset of Vim, notwithstanding some intentionally
removed misfeatures; excepting those few and carefully-considered
excisions, Neovim is Vim. It is built for users who want the good
parts of Vim, without compromise, and more.

%prep
%setup -q

%if %{without luajit}
%patch -P 1000 -p1
%endif

%build
HOSTNAME=neovim
USERNAME=neovim
source /opt/rh/gcc-toolset-10/enable
mkdir .deps
cd .deps
cmake3 ../cmake.deps \
	-G Ninja \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DUSE_BUNDLED=OFF \
	-DUSE_BUNDLED_LUV=ON \
	-DUSE_BUNDLED_LIBVTERM=ON \
	-DUSE_BUNDLED_TS=ON \
	-DUSE_BUNDLED_TS_PARSERS=ON \
	-DUSE_BUNDLED_LPEG=ON \
	-DUSE_BUNDLED_UTF8PROC=ON
ninja
cd ..

mkdir build
cd build
cmake3 .. \
	-G Ninja \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DENABLE_TRANSLATIONS=ON
cd ..

%install
HOSTNAME=neovim
USERNAME=neovim
source /opt/rh/gcc-toolset-10/enable
cd build
DESTDIR=%{buildroot} ninja install
cd ..

install -p -m 644 %SOURCE1 %{buildroot}%{_datadir}/nvim/sysinit.vim
install -p -m 644 %SOURCE2 %{buildroot}%{_datadir}/nvim/template.spec

desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
    runtime/nvim.desktop
install -d -m0755 %{buildroot}%{_datadir}/pixmaps
install -m0644 runtime/nvim.png %{buildroot}%{_datadir}/pixmaps/nvim.png

%fdupes %{buildroot}%{_datadir}/
# Fix exec bits
find %{buildroot}%{_datadir} \( -name "*.bat" -o -name "*.awk" \) \
    -print -exec chmod -x '{}' \;
%find_lang nvim

# Refresh documentation helptags.
%transfiletriggerin -- %{_datadir}/nvim/runtime/doc
%{_bindir}/nvim -u NONE -es -c ":helptags %{_datadir}/nvim/runtime/doc" -c ":q" &> /dev/null || :
 
%transfiletriggerpostun -- %{_datadir}/nvim/runtime/doc
> %{_datadir}/nvim/runtime/doc/tags || :
%{_bindir}/nvim -u NONE -es -c ":helptags %{_datadir}/nvim/runtime/doc" -c ":q" &> /dev/null || :
 
%files -f nvim.lang
%doc CONTRIBUTING.md MAINTAIN.md README.md
%{_bindir}/nvim
 
%dir %{_libdir}/nvim
%dir %{_libdir}/nvim/parser
%{_libdir}/nvim/parser/*.so
 
%{_mandir}/man1/nvim.1*
%{_datadir}/applications/nvim.desktop
%{_datadir}/pixmaps/nvim.png
%{_datadir}/icons/hicolor/128x128/apps/nvim.png
 
%dir %{_datadir}/nvim
%{_datadir}/nvim/sysinit.vim
%{_datadir}/nvim/template.spec
 
%dir %{_datadir}/nvim/runtime
%{_datadir}/nvim/runtime/*.vim
%{_datadir}/nvim/runtime/filetype.lua
%{_datadir}/nvim/runtime/neovim.ico
 
%dir %{_datadir}/nvim/runtime/autoload
%{_datadir}/nvim/runtime/autoload/README.txt
%{_datadir}/nvim/runtime/autoload/*.lua
%{_datadir}/nvim/runtime/autoload/*.vim
 
%dir %{_datadir}/nvim/runtime/autoload/cargo
%{_datadir}/nvim/runtime/autoload/cargo/*.vim
 
%dir %{_datadir}/nvim/runtime/autoload/dist
%{_datadir}/nvim/runtime/autoload/dist/*.vim
 
%dir %{_datadir}/nvim/runtime/autoload/provider
%{_datadir}/nvim/runtime/autoload/provider/*.vim
%{_datadir}/nvim/runtime/autoload/provider/script_host.rb
 
%dir %{_datadir}/nvim/runtime/autoload/remote
%{_datadir}/nvim/runtime/autoload/remote/*.vim
 
%dir %{_datadir}/nvim/runtime/autoload/rust
%{_datadir}/nvim/runtime/autoload/rust/*.vim
 
%dir %{_datadir}/nvim/runtime/autoload/xml
%{_datadir}/nvim/runtime/autoload/xml/*.vim
 
%dir %{_datadir}/nvim/runtime/colors
%{_datadir}/nvim/runtime/colors/*.lua
%{_datadir}/nvim/runtime/colors/*.vim
%{_datadir}/nvim/runtime/colors/README.txt
 
%dir %{_datadir}/nvim/runtime/compiler
%{_datadir}/nvim/runtime/compiler/*.vim
%{_datadir}/nvim/runtime/compiler/README.txt
 
%dir %{_datadir}/nvim/runtime/doc
%{_datadir}/nvim/runtime/doc/*.txt
%{_datadir}/nvim/runtime/doc/tags
 
%dir %{_datadir}/nvim/runtime/ftplugin
%{_datadir}/nvim/runtime/ftplugin/*.vim
%{_datadir}/nvim/runtime/ftplugin/*.lua
%{_datadir}/nvim/runtime/ftplugin/logtalk.dict
%{_datadir}/nvim/runtime/ftplugin/README.txt
 
%dir %{_datadir}/nvim/runtime/indent
%{_datadir}/nvim/runtime/indent/Makefile
%{_datadir}/nvim/runtime/indent/README.txt
%{_datadir}/nvim/runtime/indent/*.lua
%{_datadir}/nvim/runtime/indent/*.vim
 
%dir %{_datadir}/nvim/runtime/indent/testdir/
%{_datadir}/nvim/runtime/indent/testdir/README.txt
%{_datadir}/nvim/runtime/indent/testdir/*.in
%{_datadir}/nvim/runtime/indent/testdir/*.ok
%{_datadir}/nvim/runtime/indent/testdir/*.vim
 
%dir %{_datadir}/nvim/runtime/keymap
%{_datadir}/nvim/runtime/keymap/*.vim
%{_datadir}/nvim/runtime/keymap/README.txt
 
%dir %{_datadir}/nvim/runtime/lua
%{_datadir}/nvim/runtime/lua/*.lua
 
%dir %{_datadir}/nvim/runtime/lua/vim
%{_datadir}/nvim/runtime/lua/vim/*.lua

%dir %{_datadir}/nvim/runtime/lua/vim/_ftplugin            
%{_datadir}/nvim/runtime/lua/vim/_ftplugin/*.lua
 
%dir %{_datadir}/nvim/runtime/lua/vim/_meta
%{_datadir}/nvim/runtime/lua/vim/_meta/*.lua

%dir %{_datadir}/nvim/runtime/lua/vim/deprecated            
%{_datadir}/nvim/runtime/lua/vim/deprecated/health.lua
 
%dir %{_datadir}/nvim/runtime/lua/vim/filetype
%{_datadir}/nvim/runtime/lua/vim/filetype/*.lua

%dir %{_datadir}/nvim/runtime/lua/vim/health            
%{_datadir}/nvim/runtime/lua/vim/health/*.lua
 
%dir %{_datadir}/nvim/runtime/lua/vim/func
%{_datadir}/nvim/runtime/lua/vim/func/*.lua
 
%dir %{_datadir}/nvim/runtime/lua/vim/lsp
%{_datadir}/nvim/runtime/lua/vim/lsp/*.lua
 
%dir %{_datadir}/nvim/runtime/lua/vim/lsp/_meta
%{_datadir}/nvim/runtime/lua/vim/lsp/_meta/*.lua
 
%dir %{_datadir}/nvim/runtime/lua/vim/provider
%{_datadir}/nvim/runtime/lua/vim/provider/*.lua
 
%dir %{_datadir}/nvim/runtime/lua/vim/treesitter
%{_datadir}/nvim/runtime/lua/vim/treesitter/*.lua

%dir %{_datadir}/nvim/runtime/lua/vim/treesitter/_meta            
%{_datadir}/nvim/runtime/lua/vim/treesitter/_meta/*.lua            

%dir %{_datadir}/nvim/runtime/lua/vim/ui
%dir %{_datadir}/nvim/runtime/lua/vim/ui/clipboard
%{_datadir}/nvim/runtime/lua/vim/ui/clipboard/*.lua
 
%dir %{_datadir}/nvim/runtime/pack
%dir %{_datadir}/nvim/runtime/pack/dist
%dir %{_datadir}/nvim/runtime/pack/dist/opt
 
%dir %{_datadir}/nvim/runtime/pack/dist/opt/cfilter
%dir %{_datadir}/nvim/runtime/pack/dist/opt/cfilter/plugin
%{_datadir}/nvim/runtime/pack/dist/opt/cfilter/plugin/*.lua
 
%dir %{_datadir}/nvim/runtime/pack/dist/opt/justify
%dir %{_datadir}/nvim/runtime/pack/dist/opt/justify/plugin
%{_datadir}/nvim/runtime/pack/dist/opt/justify/plugin/*.vim
 
%dir %{_datadir}/nvim/runtime/pack/dist/opt/netrw            
%{_datadir}/nvim/runtime/pack/dist/opt/netrw/LICENSE.txt            
%{_datadir}/nvim/runtime/pack/dist/opt/netrw/README.md            

%dir %{_datadir}/nvim/runtime/pack/dist/opt/netrw/autoload            
%{_datadir}/nvim/runtime/pack/dist/opt/netrw/autoload/*.vim            

%dir %{_datadir}/nvim/runtime/pack/dist/opt/netrw/doc            
%{_datadir}/nvim/runtime/pack/dist/opt/netrw/doc/*.txt            
%{_datadir}/nvim/runtime/pack/dist/opt/netrw/doc/tags            

%dir %{_datadir}/nvim/runtime/pack/dist/opt/netrw/plugin            
%{_datadir}/nvim/runtime/pack/dist/opt/netrw/plugin/*.vim            

%dir %{_datadir}/nvim/runtime/pack/dist/opt/netrw/syntax            
%{_datadir}/nvim/runtime/pack/dist/opt/netrw/syntax/*.vim            

%dir %{_datadir}/nvim/runtime/pack/dist/opt/nohlsearch            

%dir %{_datadir}/nvim/runtime/pack/dist/opt/nohlsearch/plugin            
%{_datadir}/nvim/runtime/pack/dist/opt/nohlsearch/plugin/*.vim            

%dir %{_datadir}/nvim/runtime/pack/dist/opt/shellmenu
%dir %{_datadir}/nvim/runtime/pack/dist/opt/shellmenu/plugin
%{_datadir}/nvim/runtime/pack/dist/opt/shellmenu/plugin/*.vim
 
%dir %{_datadir}/nvim/runtime/pack/dist/opt/matchit
%dir %{_datadir}/nvim/runtime/pack/dist/opt/matchit/autoload
%{_datadir}/nvim/runtime/pack/dist/opt/matchit/autoload/*.vim
%dir %{_datadir}/nvim/runtime/pack/dist/opt/matchit/doc
%{_datadir}/nvim/runtime/pack/dist/opt/matchit/doc/matchit.txt
%{_datadir}/nvim/runtime/pack/dist/opt/matchit/doc/tags
%dir %{_datadir}/nvim/runtime/pack/dist/opt/matchit/plugin
%{_datadir}/nvim/runtime/pack/dist/opt/matchit/plugin/*.vim
 
%dir %{_datadir}/nvim/runtime/pack/dist/opt/swapmouse
%dir %{_datadir}/nvim/runtime/pack/dist/opt/swapmouse/plugin
%{_datadir}/nvim/runtime/pack/dist/opt/swapmouse/plugin/*.vim
 
%dir %{_datadir}/nvim/runtime/pack/dist/opt/termdebug
%dir %{_datadir}/nvim/runtime/pack/dist/opt/termdebug/plugin
%{_datadir}/nvim/runtime/pack/dist/opt/termdebug/plugin/*.vim
 
%dir %{_datadir}/nvim/runtime/plugin
%{_datadir}/nvim/runtime/plugin/*.lua
%{_datadir}/nvim/runtime/plugin/*.vim
 
%dir %{_datadir}/nvim/runtime/queries/
 
%dir %{_datadir}/nvim/runtime/queries/c
%{_datadir}/nvim/runtime/queries/c/*.scm
 
%dir %{_datadir}/nvim/runtime/queries/lua/
%{_datadir}/nvim/runtime/queries/lua/folds.scm
%{_datadir}/nvim/runtime/queries/lua/highlights.scm
%{_datadir}/nvim/runtime/queries/lua/injections.scm
 
%dir %{_datadir}/nvim/runtime/queries/markdown
%{_datadir}/nvim/runtime/queries/markdown/*.scm
 
%dir %{_datadir}/nvim/runtime/queries/markdown_inline
%{_datadir}/nvim/runtime/queries/markdown_inline/*.scm
 
%dir %{_datadir}/nvim/runtime/queries/query
%{_datadir}/nvim/runtime/queries/query/*.scm
 
%dir %{_datadir}/nvim/runtime/queries/vim/
%{_datadir}/nvim/runtime/queries/vim/*.scm
 
%dir %{_datadir}/nvim/runtime/queries/vimdoc/
%{_datadir}/nvim/runtime/queries/vimdoc/*.scm

%dir %{_datadir}/nvim/runtime/scripts            
%{_datadir}/nvim/runtime/scripts/*.lua            
%{_datadir}/nvim/runtime/scripts/*.vim            
%{_datadir}/nvim/runtime/scripts/less.bat            
%{_datadir}/nvim/runtime/scripts/less.sh            
 
%dir %{_datadir}/nvim/runtime/spell
%{_datadir}/nvim/runtime/spell/cleanadd.vim
%{_datadir}/nvim/runtime/spell/en.utf-8.spl
 
%dir %{_datadir}/nvim/runtime/syntax
%{_datadir}/nvim/runtime/syntax/*.lua
%{_datadir}/nvim/runtime/syntax/*.vim
%{_datadir}/nvim/runtime/syntax/README.txt
 
%dir %{_datadir}/nvim/runtime/syntax/modula2
%dir %{_datadir}/nvim/runtime/syntax/modula2/opt
%{_datadir}/nvim/runtime/syntax/modula2/opt/*.vim
 
%dir %{_datadir}/nvim/runtime/syntax/vim
%{_datadir}/nvim/runtime/syntax/vim/generated.vim
 
%dir %{_datadir}/nvim/runtime/syntax/shared
%{_datadir}/nvim/runtime/syntax/shared/*.vim
%{_datadir}/nvim/runtime/syntax/shared/README.txt
 
%dir %{_datadir}/nvim/runtime/tutor
%{_datadir}/nvim/runtime/tutor/tutor.tutor
%{_datadir}/nvim/runtime/tutor/tutor.tutor.json
 
%dir %{_datadir}/nvim/runtime/tutor/en
%{_datadir}/nvim/runtime/tutor/en/vim-01-beginner.tutor
%{_datadir}/nvim/runtime/tutor/en/vim-01-beginner.tutor.json
 
%dir %{_datadir}/nvim/runtime/tutor/ja
%{_datadir}/nvim/runtime/tutor/ja/vim-01-beginner.tutor
%{_datadir}/nvim/runtime/tutor/ja/vim-01-beginner.tutor.json

%changelog
* Fri Apr 04 2025 Danilo Petkovic <petkovicdanilo97@gmail.com> - 0.11.0-1
- Update to 0.11.0

* Wed Jan 01 2025 Danilo Petkovic <petkovicdanilo97@gmail.com> - 0.10.4-1
- Update to 0.10.4

* Sat Dec 28 2024 Danilo Petkovic <petkovicdanilo97@gmail.com> - 0.10.3-1
- Initial version
