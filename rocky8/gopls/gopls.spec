%define debug_package %{nil}

Name:           gopls
Version:        0.18.1
Release:        1%{?dist}
Summary:        gopls, the Go language server

License:        BSD-3-Clause
URL:            https://github.com/golang/tools/
Source0:	https://github.com/golang/tools/archive/refs/tags/gopls/v%{version}.tar.gz

# golang also required for build, but not provided through RPM

%description
gopls (pronounced "Go please") is the official Go language server developed by the Go team.
It provides a wide variety of IDE features to any LSP-compatible editor.

You should not need to interact with gopls directly--it will be automatically integrated into
your editor. The specific features and settings vary slightly by editor, so we recommend that
you proceed to the documentation for your editor below.
Also, the gopls documentation for each feature describes whether it is supported in
each client editor.

%prep
%setup -q -n tools-gopls-v%{version}

%build
cd gopls
PATH=$PATH:/usr/local/go/bin go build -ldflags="-X 'main.version=v%{version}'"

%install
rm -rf %{buildroot}

install -vdm 0755 %{buildroot}%{_bindir}
install -vDpm 0755 gopls/gopls %{buildroot}%{_bindir}/

%post

%postun

%files

%license LICENSE
%doc gopls/README.md CONTRIBUTING.md

%{_bindir}/gopls

%changelog
* Sat Mar 22 2024 Danilo Petkovic <petkovicdanilo97@gmail.com> - 0.18.1-1
- Update to 0.18.1

* Sun Dec 29 2024 Danilo Petkovic <petkovicdanilo97@gmail.com> - 0.17.1-1
- Initial RPM release.

