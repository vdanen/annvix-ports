#
# spec file for ports package pdns
#
# Ports Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments to the maintainer of this package:
#
#   vdanen@annvix.org
#
# $Id$


%define name		pdns
%define version		2.9.17
%define release		7avx

%define _prefix		/usr/local
%define _mandir		/usr/local/share/man
%define _infodir	/usr/local/share/info
%define _sysconfdir	/usr/local/etc
%define _docdir		/usr/local/share/doc

Summary:	PowerDNS is a versatile database-driven nameserver
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.powerdns.com/
Source0:	http://downloads.powerdns.com/releases/%{name}-%{version}.tar.gz
Source1:	pdns.run
Source2:	pdns-log.run
Source3:	pdnsr.run
Source4:	pdnsr-log.run
Patch1:		pdns-2.9.17-avoid-version.diff
Patch2:		pdns-2.9.17-no_libpq++.diff
Patch3:		pdns-2.9.17-cvs-x86_64.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	MySQL-devel, postgresql-devel
#BuildRequires:	openldap-devel
BuildRequires:	bison, flex, gdbm-devel, libstdc++-devel, openssl-devel, zlib-devel
BuildRequires:	autoconf2.5, automake1.7

PreReq:		rpm-helper
Provides:	nameserver powerdns
Obsoletes:	nameserver powerdns

%description
PowerDNS is a versatile nameserver which supports a large number
of different backends ranging from simple zonefiles to relational
databases and load balancing/failover algorithms.

This RPM is statically compiled and should work on all Linux distributions.
It comes with support for MySQL, PostgreSQL, Bind zonefiles and the 'pipe
backend' availible as external packages.


%package recursor
Summary:	Recursor for %{name}
Group:		System/Servers
PreReq:		rpm-helper
Requires:	%{name} = %{version}

%description recursor
This package contains a recursor for the PowerDNS nameserver.  This can
allow PowerDNS to provide caching nameserver services.


%package backend-mysql
Summary:	MySQL backend for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}

%description backend-mysql
This package contains a MySQL backend for the PowerDNS nameserver.


%package backend-pgsql
Summary:	Generic PostgreSQL backend for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}

%description backend-pgsql
This package contains a generic PostgreSQL backend 
for the PowerDNS nameserver. It has configurable SQL statements.


#%package backend-ldap
#Summary:	LDAP backend for %{name}
#Group:		System/Servers
#Requires:	%{name} = %{version}
#
#%description backend-ldap
#This package contains a LDAP backend for the PowerDNS nameserver.


%package	devel
Summary:	Development headers and libraries for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}
Requires:	%{name}-backend-mysql = %{version}
Requires:	%{name}-backend-pgsql = %{version}
#Requires:	%{name}-backend-ldap = %{version}

%description devel
Development headers and libraries for %{name}


%prep
%setup -q -n %{name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1 -b .x86_64


%build
#%%define __libtoolize /bin/true
export WANT_AUTOCONF_2_5=1
touch NEWS AUTHORS
libtoolize --copy --force; aclocal-1.7; autoconf; automake-1.7 --copy --add-missing

%configure2_5x \
    --sysconfdir=%{_sysconfdir}/pdns \
    --libdir=%{_libdir}/pdns \
    --with-socketdir=/var/run/pdns \
    --with-dynmodules="gmysql gpgsql pipe" \
    --with-modules="" \
    --with-mysql=/usr --with-mysql-lib=/usr/%{_lib} --with-mysql-includes=/usr/include/mysql \
    --with-pgsql=/usr --with-pgsql-lib=/usr/%{_lib} --with-pgsql-includes=/usr/include//pgsql\
    --enable-recursor
#   --with-dynmodules="gmysql gpgsql pipe ldap"

# why is this nessesary all of a sudden?
find . -type f -name "Makefile" | xargs perl -pi -e "s|-pthread|-lpthread|g"

# parallell build's broken now?
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

mkdir -p %{buildroot}/var/run/pdns

# fix the config
mv %{buildroot}%{_sysconfdir}/pdns/pdns.conf-dist %{buildroot}%{_sysconfdir}/pdns/pdns.conf

cat >> %{buildroot}%{_sysconfdir}/pdns/pdns.conf << EOF
module-dir=%{_libdir}/pdns
socket-dir=/var/run/pdns
config-dir=%{_sysconfdir}/pdns
setuid=pdns
setgid=pdns
launch=bind
daemon=no
guardian=yes
#recursor=127.0.0.1:5300
EOF

cat >> %{buildroot}%{_sysconfdir}/pdns/recursor.conf << EOF
soa-minimum-ttl=0
soa-serial-offset=0
aaaa-additional-processing=off
local-port=5300
local-address=127.0.0.1
trace=off
daemon=no
quiet=on
EOF

chmod 0600 %{buildroot}%{_sysconfdir}/pdns/pdns.conf
chmod 0644 %{buildroot}%{_sysconfdir}/pdns/recursor.conf

cat >> README.recursor << EOF
NOTE: This is still experimental...

To enable the recursor for the PowerDNS server issue the command:

echo "recursor=127.0.0.1:5300" >> %{_sysconfdir}/pdns/pdns.conf

And restart PowerDNS
EOF

mkdir -p %{buildroot}%{_srvdir}/{pdns,pdnsr}/log
install -m 0740 %{SOURCE1} %{buildroot}%{_srvdir}/pdns/run
install -m 0740 %{SOURCE2} %{buildroot}%{_srvdir}/pdns/log/run
install -m 0740 %{SOURCE3} %{buildroot}%{_srvdir}/pdnsr/run
install -m 0740 %{SOURCE4} %{buildroot}%{_srvdir}/pdnsr/log/run


%pre
%_pre_useradd pdns /var/lib/pdns /bin/false 88

%post
if [ -d /var/log/supervise/pdns -a ! -d /var/log/service/pdns ]; then
    mv /var/log/supervise/pdns /var/log/service/
fi
%_post_srv pdns

%preun
%_preun_srv pdns

%postun
%_postun_userdel pdns

%post recursor
if [ -d /var/log/supervise/pdnsr -a ! -d /var/log/service/pdnsr ]; then
    mv /var/log/supervise/pdnsr /var/log/service/
fi
%_post_srv pdnsr

%preun recursor
%_preun_srv pdnsr


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc ChangeLog HACKING INSTALL README TODO WARNING
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/pdns/pdns.conf
%dir %{_sysconfdir}/pdns
%dir %{_libdir}/pdns
%{_libdir}/pdns/libpipebackend.so
%dir %attr(0755,pdns,pdns) /var/run/pdns
%{_bindir}/pdns_control
%{_bindir}/zone2sql
%{_bindir}/zone2ldap
%{_sbindir}/pdns_server
%{_mandir}/man8/pdns_control.8*
%{_mandir}/man8/pdns_server.8*
%{_mandir}/man8/zone2sql.8*
%dir %attr(0750,root,admin) %{_srvdir}/pdns
%dir %attr(0750,root,admin) %{_srvdir}/pdns/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/pdns/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/pdns/log/run

%files recursor
%defattr(-,root,root)
%doc README.recursor
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/pdns/recursor.conf
%{_sbindir}/pdns_recursor
%dir %attr(0750,root,admin) %{_srvdir}/pdnsr
%dir %attr(0750,root,admin) %{_srvdir}/pdnsr/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/pdnsr/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/pdnsr/log/run

%files backend-mysql
%defattr(-,root,root)
%{_libdir}/pdns/libgmysqlbackend.so

%files backend-pgsql
%defattr(-,root,root)
%{_libdir}/pdns/libgpgsqlbackend.so

#%files backend-ldap
#%defattr(-,root,root)
#%{_libdir}/pdns/libldapbackend.so

%files devel
%defattr(-,root,root)
#%{_libdir}/pdns/*.so
%{_libdir}/pdns/*.la
%{_libdir}/pdns/*.a


%changelog
* Sat Sep 03 2005 Vincent Danen <vdanen@annvix.org> 2.9.17-7avx
- use execlineb for run scripts
- move logdir to /var/log/service/{pdns,pdnsr}
- run scripts are now considered config files and are not replaceable
- don't build with ldap for now; it doesn't like openldap 2.3.6
- this is in ports now

* Sat Aug 27 2005 Vincent Danen <vdanen@annvix.org> 2.9.17-6avx
- fix perms on run scripts

* Fri Aug 19 2005 Vincent Danen <vdanen@annvix.org> 2.9.17-5avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen@annvix.org> 2.9.17-4avx
- rebuild

* Thu Mar 03 2005 Vincent Danen <vdanen@annvix.org> 2.9.17-3avx
- use logger for logging

* Sat Feb 13 2005 Vincent Danen <vdanen@annvix.org> 2.9.17-2avx
- P3: x86_64 fixes from pdns dev branch

* Wed Feb 09 2005 Vincent Danen <vdanen@annvix.org> 2.9.17-1avx
- first Annvix build
- s/powerdns/pdns/ all over the place
- drop initscripts
- drop all backends but mysql, pgsql, ldap, pipe, and bind
- drop backend-pipe sub-package, pipe is in main package now
- don't package all the html docs
- user pdns has static uid/gid 88
- run scripts
- call the recursor/cache service pdnsr rather than pdns_recursor

* Mon Jan 24 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.9.17-3mdk
- rebuilt against MySQL-4.1.x and PostgreSQL-8.x system libs

* Thu Jan 13 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.9.17-2mdk
- added the forgotten geo backend sub package
- added new docs

* Wed Jan 12 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.9.17-1mdk
- 2.9.17
- rediffed P1 & P2
- drop P3, it's included

* Sat Jul 31 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.9.16-2mdk
- rebuilt against new deps and with gcc v3.4.x
- remove obsolete pq++ requirements (new P2)
- added P3
- use libtool magic
- misc spec file fixes

* Fri Apr 16 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.9.16-1mdk
- 2.9.16
- rediffed P1

* Thu Dec 18 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9.13-1mdk
- 2.9.13
- new S1, added P2

* Fri Oct 31 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9.12-1mdk
- 2.9.12
- sqlite support, new S1, added P1
- drop the static-devel sub package
- fix explicit-lib-dependency & invalid-build-requires
- thanks to Charles A Edwards for reminding me about the libtool stuff

* Sat Aug 23 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9.11-1mdk
- 2.9.11

* Wed Jul 16 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9.10-1mdk
- 2.9.10
- rebuilt against new openldap, etc.
- spec file hack to make it build
- new S1
- no linking against sasl is done here, so remove this dependency

* Sun Jun 29 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9.8-2mdk
- built against new PostgreSQL libs
- use macros
- misc spec file fixes

* Fri May 02 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9.8-1mdk
- 2.9.8
- new S1
- misc spec file fixes

* Sat Mar 29 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9.7-3mdk
- fix S2 (run as the powerdns user, thanks bugzilla-mandrake@bkor.dhs.org)
- fix P0 to reflect socketdir location

* Wed Mar 26 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9.7-2mdk
- fix #3517 (as an optional subpackage)
- fix socketdir

* Sun Mar 23 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9.7-1mdk
- 2.9.7
- fresh S1

* Tue Mar 11 2003 Marcel Pol <mpol@gmx.net> 2.9.6-3mdk
- conflicts: tmdns

* Mon Mar 10 2003 Marcel Pol <mpol@gmx.net> 2.9.6-2mdk
- buildreq: libgdbm2-devel

* Mon Feb 17 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9.6-1mdk
- 2.9.6
- added the backend-ldap sub package
- misc spec file fixes
- built against latest requires and buildrequires

* Sat Jan 18 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9.4-1mdk
- 2.9.4
- added missing stuff in %{_bindir}/
- broke out the modules into separate sub packages, used the
  debian descriptions
- added development sub packages
- misc spec file fixes

* Tue Dec 17 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9.2-1mdk
- initial cooker contrib (i cross my fingers that it works on first try...)
