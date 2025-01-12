%define debug_package %{nil}

Name:    zsh-completions
Version: 0.35.0
Release: 1%{?dist}

Summary: Additional completion definitions for Zsh
License: ZSH licence
URL:     https://github.com/zsh-users/zsh-completions
Source0: https://github.com/zsh-users/%{name}/archive/refs/tags/%{version}.tar.gz

BuildArch: noarch

BuildRequires: zsh
Requires: zsh

%description
Additional completion definitions for Zsh.

This projects aims at gathering/developing new completion scripts that are not available in Zsh yet. The scripts may be contributed to the Zsh project when stable enough.

%prep
%setup -q -n %{name}-%{version}

%build

%install
rm -rf %{buildroot}
install -Dpm 0755 zsh-completions.plugin.zsh -t %{buildroot}%{_datadir}/zsh-completions
install -d %{buildroot}%{_datadir}/zsh-completions/src
install -Dpm 0664 src/* -t %{buildroot}%{_datadir}/zsh-completions/src

%check

%files
%doc README.md
%doc CONTRIBUTING.md
%license LICENSE

%{_datadir}/zsh-completions/zsh-completions.plugin.zsh
%{_datadir}/zsh-completions/src/*

%changelog
* Sun Jan 12 2025 Danilo Petkovic <petkovicdanilo97@gmail.com> - 0.35.0-1
- Initial RPM release.
