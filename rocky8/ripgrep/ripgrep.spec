%define debug_package %{nil}

Name:           ripgrep
Version:        14.1.1
Release:        1%{?dist}
Summary:        ripgrep recursively searches directories for a regex pattern while respecting your gitignore

License:        Unlicense OR MIT
URL:            https://github.com/BurntSushi/ripgrep
Source0:        https://github.com/BurntSushi/ripgrep/archive/refs/tags/%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
# rust also required for build, but not provided through RPM

%description
ripgrep is a line-oriented search tool that recursively searches the current directory for a regex pattern.
By default, ripgrep will respect gitignore rules and automatically skip hidden files/directories and binary files.
(To disable all automatic filtering by default, use rg -uuu.) ripgrep has first class support on Windows, macOS 
and Linux, with binary downloads available for every release. 
ripgrep is similar to other popular search tools like The Silver Searcher, ack and grep.

%prep
%setup -q

%build
source ~/.cargo/env
cargo build --release --features pcre2

%install
rm -rf %{buildroot}
install -Dpm 0755 target/release/rg -t %{buildroot}%{_bindir}

# generate and install manpage
target/release/rg --generate man > rg.1
install -Dpm 0644 rg.1 -t %{buildroot}%{_mandir}/man1/

# generate and install shell completions
target/release/rg --generate complete-bash > rg.bash
target/release/rg --generate complete-fish > rg.fish
target/release/rg --generate complete-zsh > _rg

install -Dpm 0644 rg.bash -t %{buildroot}%{_datadir}/bash-completion/completions
install -Dpm 0644 rg.fish -t %{buildroot}%{_datadir}/fish/vendor_completions.d
install -Dpm 0644 _rg -t %{buildroot}%{_datadir}/zsh/site-functions

%post

%postun

%files
%license COPYING
%license LICENSE-MIT
%license UNLICENSE

%doc CHANGELOG.md
%doc FAQ.md
%doc GUIDE.md
%doc README.md
%doc RELEASE-CHECKLIST.md

%{_bindir}/rg
%{_mandir}/man1/rg.1*
%{_datadir}/bash-completion/completions/rg.bash
%{_datadir}/fish/vendor_completions.d/rg.fish
%{_datadir}/zsh/site-functions/_rg

%changelog
* Sun Dec 29 2024 Danilo Petkovic <petkovicdanilo97@gmail.com> - 14.1.1-1
- Initial RPM release.

