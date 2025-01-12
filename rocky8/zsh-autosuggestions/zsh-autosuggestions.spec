%define debug_package %{nil}

Name:    zsh-autosuggestions
Version: 0.7.1
Release: 1%{?dist}

Summary: Fish-like autosuggestions for zsh
License: MIT
URL:     https://github.com/zsh-users/zsh-autosuggestions
Source0: https://github.com/zsh-users/%{name}/archive/refs/tags/v%{version}.tar.gz

BuildArch: noarch

BuildRequires: make
BuildRequires: zsh

Requires: zsh

%description
This package provides autosuggestions for the shell zsh. It suggests commands
as you type based on history and completions.

%prep
%autosetup

%build
make

%install
install -D --preserve-timestamps --target-directory=%{buildroot}%{_datadir}/%{name} %{name}.zsh

%check

%files
%doc CHANGELOG.md README.md
%license LICENSE
%{_datadir}/%{name}

%changelog
* Sun Jan 12 2025 Danilo Petkovic <petkovicdanilo97@gmail.com> - 0.7.1-1
- Initial RPM release.

