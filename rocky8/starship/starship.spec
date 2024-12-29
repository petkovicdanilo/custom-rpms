%define debug_package %{nil}

Name:           starship
Version:        1.21.1
Release:        1%{?dist}
Summary:        A modern alternative to ls

License:        EUPL-1.2
URL:            https://github.com/starship/starship
Source0:        https://github.com/%{name}/%{name}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
# rust also required for build, but not provided through RPM

%description
The minimal, blazing-fast, and infinitely customizable prompt for any shell!

- Fast: it's fast – really really fast!
- Customizable: configure every aspect of your prompt.
- Universal: works on any shell, on any operating system.
- Intelligent: shows relevant information at a glance.
- Feature rich: support for all your favorite tools.
- Easy: quick to install – start using it in minutes

%prep
%setup -q

%build
source ~/.cargo/env
cargo build --release

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
cp target/release/starship %{buildroot}%{_bindir}

%post

%postun

%files
%{_bindir}/starship

%changelog
* Sun Dec 29 2024 Danilo Petkovic <petkovicdanilo97@gmail.com> - 1.21.1-1
- Initial RPM release.

