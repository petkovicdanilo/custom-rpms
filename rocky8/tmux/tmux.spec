%define debug_package %{nil}

Name:           tmux
Version:        3.5a
Release:        1%{?dist}
Summary:        A terminal multiplexer
 
Group:          Applications/System
# Most of the source is ISC licensed; some of the files in compat/ are 2 and
# 3 clause BSD licensed.
License:        ISC and BSD
URL:            http://sourceforge.net/projects/tmux
Source0:        https://github.com/%{name}/%{name}/archive/refs/tags/%{version}.tar.gz
Source1:        bash_completion_tmux.sh
Source2:        tmux@.service

Patch1000:      systemd.patch
 
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  automake
BuildRequires:  byacc
BuildRequires:  ncurses-devel
BuildRequires:  libevent-devel
BuildRequires:  libutempter-devel
BuildRequires:  systemd-devel
BuildRequires:  jemalloc-devel
 
%description
tmux is a terminal multiplexer: it enables a number of terminals to be created,
accessed, and controlled from a single screen. tmux may be detached from a screen and 
continue running in the background, then later reattached.
 
%prep
%setup -q

%patch -P 1000 -p1
 
%build
./autogen.sh
./configure --prefix=%{_prefix} --enable-sixel --enable-utempter --enable-systemd --enable-jemalloc
make
 
%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALLBIN="install -p -m 755" INSTALLMAN="install -p -m 644"
install -Dpm 644 %{SOURCE1} %{buildroot}%{_datadir}/bash-completion/completions/tmux
install -Dpm 644 %{SOURCE2} %{buildroot}%{_unitdir}/tmux@.service
 
%post
if [ ! -f %{_sysconfdir}/shells ] ; then
    echo "%{_bindir}/tmux" > %{_sysconfdir}/shells
else
    grep -q "^%{_bindir}/tmux$" %{_sysconfdir}/shells || echo "%{_bindir}/tmux" >> %{_sysconfdir}/shells
fi
 
%postun
if [ $1 -eq 0 ] && [ -f %{_sysconfdir}/shells ]; then
    sed -i '\!^%{_bindir}/tmux$!d' %{_sysconfdir}/shells
fi

%files
%license COPYING
%doc CHANGES README* example_tmux.conf
%{_bindir}/tmux
%{_mandir}/man1/tmux.1.*
%{_datadir}/bash-completion/completions/tmux
%{_unitdir}/tmux@.service

%changelog
* Fri Dec 27 2024 Danilo Petkovic <petkovicdanilo97@gmail.com> - 3.5a-1
- Initial RPM release.
 
