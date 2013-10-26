# TODO
# - crontab spool dir not compatible with other cron implementations
# - package default hourly,monhtly,etc and provide crontabs name
# - provides anacron functionality, O/P name?
# - triggers for switching with other crondaemons (after testing)
# - logrotate?
# - systemd init
# - crontab system group
Summary:	Lightweight Cron Daemon
Name:		dcron
Version:	4.5
Release:	0.1
License:	GPL v2+
Group:		Daemons
Source0:	http://www.jimpryor.net/linux/releases/%{name}-%{version}.tar.gz
# Source0-md5:	078833f3281f96944fc30392b1888326
Source1:	%{name}.init
Patch1:		%{name}-fix_makefile.patch
URL:		http://www.jimpryor.net/linux/dcron.html
BuildRequires:	pkgconfig
Provides:	crondaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This lightweight cron daemon aims to be simple and secure, with just
enough features to stay useful. It was written from scratch by Matt
Dillon in 1994. It's now developed and maintained by Jim Pryor.

In the author's opinion, having to combine a cron daemon with another
daemon like anacron makes for too much complexity. So the goal is a
simple cron daemon that can also take over the central functions of
anacron.

%prep
%setup -q
%patch1

%build
%{__make} \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags}" \
	PREFIX=%{_prefix} \
	INSTALL="install -p"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,cron.d}
%{__make} install \
    DESTDIR=$RPM_BUILD_ROOT

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/crond
install -d $RPM_BUILD_ROOT%{_var}/spool/%{name}/{crontabs,cronstamps}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG README
%dir /etc/cron.d
%attr(754,root,root) /etc/rc.d/init.d/crond
%attr(755,root,root) %{_bindir}/crontab
%attr(755,root,root) %{_sbindir}/crond
%{_mandir}/man1/crontab.1.*
%{_mandir}/man8/crond.8.*
%dir %attr(700,root,root) %{_var}/spool/%{name}
%dir %attr(700,root,root) %{_var}/spool/%{name}/crontabs
%dir %attr(700,root,root) %{_var}/spool/%{name}/cronstamps
