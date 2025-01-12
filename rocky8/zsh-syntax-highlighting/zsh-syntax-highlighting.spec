%define debug_package %{nil}

Name:    zsh-syntax-highlighting
Version: 0.8.0
Release: 1%{?dist}

Summary: Fish shell like syntax highlighting for Zsh
License: BSD
URL:     https://github.com/zsh-users/zsh-syntax-highlighting
Source0: https://github.com/zsh-users/%{name}/archive/refs/tags/%{version}.tar.gz

BuildArch: noarch

BuildRequires: make
BuildRequires: zsh

Requires: zsh

%description
This package provides syntax highlighting for the shell zsh. It enables
highlighting of commands whilst they are typed at a zsh prompt into an
interactive terminal. This helps in reviewing commands before running them,
particularly in catching syntax errors.

%prep
%setup -q -n %{name}-%{version}

%build
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} PREFIX=%{_prefix}
rm %{buildroot}/%{_docdir}/%{name}/COPYING.md

%check
#make test
#make perf

%files
%doc INSTALL.md
%license COPYING.md
%{_docdir}/%{name}
%{_datadir}/%{name}

%changelog
* Sun Jan 12 2025 Danilo Petkovic <petkovicdanilo97@gmail.com> - 0.8.0-1
- Initial RPM release.
