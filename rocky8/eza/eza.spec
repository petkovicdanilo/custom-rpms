%define debug_package %{nil}

Name:           eza
Version:        0.20.14
Release:        1%{?dist}
Summary:        A modern alternative to ls

License:        EUPL-1.2
URL:            https://github.com/%{name}-community/%{name}
Source0:        https://github.com/%{name}-community/%{name}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  gcc
# justfile and rust also required for build, but not provided through RPMs

%description
eza is a modern alternative for the venerable file-listing command-line program ls that ships
with Unix and Linux operating systems, giving it more features and better defaults.
It uses colours to distinguish file types and metadata. It knows about symlinks, extended 
attributes, and Git. And it’s small, fast, and just one single binary.

By deliberately making some decisions differently, eza attempts to be a more featureful,
more user-friendly version of ls. 

%prep
%setup -q

%build
source ~/.cargo/env
just build-release
just man

%install
rm -rf %{buildroot}
install -Dpm 0755 target/release/eza -t %{buildroot}%{_bindir}

install -Dpm 0644 target/man/*.1 -t %{buildroot}%{_mandir}/man1/
install -Dpm 0644 target/man/*.5 -t %{buildroot}%{_mandir}/man5/

%post

%postun

%files
%license LICENSE.txt

%doc CHANGELOG.md
%doc CODE_OF_CONDUCT.md
%doc CONTRIBUTING.md
%doc README.md
%doc SECURITY.md
%doc TESTING.md

%{_bindir}/eza
%{_mandir}/man1/eza.1.*
%{_mandir}/man5/eza_colors-explanation.5.*
%{_mandir}/man5/eza_colors.5.*

%changelog
* Sun Dec 29 2024 Danilo Petkovic <petkovicdanilo97@gmail.com> - 0.20.14-1
- Initial RPM release.

