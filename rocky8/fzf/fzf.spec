%define debug_package %{nil}

Name:           fzf
Version:        0.59.0
Release:        1%{?dist}
Summary:        A command-line fuzzy finder

License:        MIT
URL:            https://github.com/junegunn/%{name}
Source0:        https://github.com/junegunn/%{name}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
# golang also required for build, but not provided through RPM

%description
fzf is a general-purpose command-line fuzzy finder.

It's an interactive filter program for any kind of list; files, command history, processes, hostnames, bookmarks, git commits, etc. It implements a "fuzzy" matching algorithm, so you can quickly type in patterns with omitted characters and still get the results you want.

%prep
%setup -q

%build
PATH=$PATH:/usr/local/go/bin FZF_VERSION=%{version} FZF_REVISION=tarball make install

%install
rm -rf %{buildroot}

install -vdm 0755 %{buildroot}%{_bindir}
install -vDpm 0755 bin/* %{buildroot}%{_bindir}/
install -d -p %{buildroot}%{_mandir}/man1
install -Dpm0644 man/man1/*.1 %{buildroot}%{_mandir}/man1/

install -d %{buildroot}%{_datadir}/fzf

# Install shell completion
install -d %{buildroot}%{_sysconfdir}/bash_completion.d/
install -Dpm0644 shell/completion.bash %{buildroot}%{_sysconfdir}/bash_completion.d/fzf
install -d %{buildroot}%{_datadir}/zsh/site-functions
install -Dpm0644 shell/completion.zsh %{buildroot}%{_datadir}/zsh/site-functions/fzf

# Install shell key bindings
install -d %{buildroot}%{_datadir}/fzf/shell
install -Dpm0644 shell/key-bindings.* %{buildroot}%{_datadir}/fzf/shell/

%post

%postun

%files

%license LICENSE
%doc README.md CHANGELOG.md

%{_bindir}/fzf
%{_bindir}/fzf-tmux
%{_bindir}/fzf-preview.sh
%{_mandir}/man1/fzf.1.*
%{_mandir}/man1/fzf-tmux.1.*
%{_sysconfdir}/bash_completion.d/fzf
%{_datadir}/zsh/site-functions/fzf
%{_datadir}/fzf/shell/*

%changelog
* Sun Feb 09 2025 Danilo Petkovic <petkovicdanilo97@gmail.com> - 0.59.0-1
- Update to 0.59.0

* Sat Jan 01 2025 Danilo Petkovic <petkovicdanilo97@gmail.com> - 0.58.0-1
- Update to 0.58.0

* Sun Dec 29 2024 Danilo Petkovic <petkovicdanilo97@gmail.com> - 0.57.0-1
- Initial RPM release.

