%define debug_package %{nil}

Name:    zsh-vi-mode
Version: 0.11.0
Release: 1%{?dist}

Summary: A better and friendly vi(vim) mode plugin for ZSH.
License: MIT
URL:     https://github.com/jeffreytse/zsh-vi-mode
Source0: https://github.com/jeffreytse/%{name}/archive/refs/tags/v%{version}.tar.gz

BuildArch: noarch

BuildRequires: zsh

Requires: zsh

%description
Maybe you have experienced the default Vi mode in Zsh, after turning on the default Vi mode, you gradually found that it had many problems, some features were not perfect or non-existent, and some behaviors even were different from the native Vi(Vim) mode.

Although the default Vi mode was a bit embarrassing and unpleasant, you kept on using it and gradually lost your interest on it after using for a period of time. Eventually, you disappointedly gave up.

You never think of the Vi mode for a long time, one day you accidentally discovered this plugin, you read here and realize that this plugin is to solve the above problems and make you fall in love to Vi mode again. A smile suddenly appeared on your face like regaining a good life.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}

install -Dpm 0755 %{name}.plugin.zsh -t %{buildroot}%{_datadir}/%{name}
install -Dpm 0755 %{name}.zsh -t %{buildroot}%{_datadir}/%{name}

%check

%files
%doc README.md
%license LICENSE

%{_datadir}/%{name}/%{name}.plugin.zsh
%{_datadir}/%{name}/%{name}.zsh

%changelog
* Wed Jan 15 2025 Danilo Petkovic <petkovicdanilo97@gmail.com> - 0.11.0-1
- Initial RPM release.
