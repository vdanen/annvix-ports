#
# spec file for ports package daemontools
#
# Ports Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments to the maintainer of this package:
#
#   vdanen@annvix.org
#
# $Id$


%define name		daemontools
%define version		0.76
%define release		12avx

%define _prefix		/usr/local
%define _mandir		/usr/local/share/man
%define _infodir	/usr/local/share/info
%define _sysconfdir	/usr/local/etc
%define _docdir		/usr/local/share/doc

Summary:	DJB daemontools
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	D. J. Bernstein
Group:		System/Servers
URL:		http://cr.yp.to/daemontools.html
Source0:	http://cr.yp.to/daemontools/%{name}-%{version}.tar.gz
Source1:	http://smarden.org/pape/djb/manpages/%{name}-%{version}-man.tar.gz
Patch0:		daemontools-0.76-errno.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
 
%description
supervise monitors a service. It starts the service and restarts the
service if it dies. The companion svc program stops, pauses, or restarts
the service on sysadmin request. The svstat program prints a one-line
status report.

multilog saves error messages to one or more logs.  It optionally timestamps
each line and, for each log, includes or excludes lines matching specified
patterns.  It automatically rotates logs to limit the amount of disk space
used.  If the disk fills up, it pauses and tries again, without losing any
data.


%prep
%setup -q -n admin
%setup -q -a 1 -n admin/%{name}-%{version}
%patch0 -p1 -b .errno


%build
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}

echo "gcc %{optflags}" >src/conf-cc
echo "gcc -s %{optflags}" >src/conf-ld
echo "%{_prefix}" >src/conf-home

package/compile


%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man8

install -s -m 0755 command/* %{buildroot}%{_bindir}
install -m 0644 %{name}-man/*.8 %{buildroot}%{_mandir}/man8/

# move some docs
mv src/CHANGES .
mv package/README .
mv src/TODO .


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr (-,root,root)
%doc CHANGES README TODO
%{_bindir}/svscan
%{_bindir}/svscanboot
%{_bindir}/supervise
%{_bindir}/svc
%{_bindir}/svok
%{_bindir}/svstat
%{_bindir}/fghack
%{_bindir}/multilog
%{_bindir}/pgrphack
%{_bindir}/tai64n
%{_bindir}/tai64nlocal
%{_bindir}/readproctitle
%{_bindir}/softlimit
%{_bindir}/envuidgid
%{_bindir}/envdir
%{_bindir}/setlock
%{_bindir}/setuidgid
%{_mandir}/man8/*


%changelog
* Tue Aug 23 2005 Vincent Danen <vdanen@annvix.org> 0.76-12avx
- move to ports
- remove /command
- remove ownership of _srvdir and _srvlogdir

* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 0.76-11avx
- Annvix build

* Wed Mar 03 2004 Vincent Danen <vdanen@opensls.org> 0.76-10sls
- minor spec cleanups
- supervise macros

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 0.76-9sls
- own /var/log/supervise and /var/service

* Sun Nov 30 2003 Vincent Danen <vdanen@opensls.org> 0.76-8sls
- OpenSLS build
- tidy spec

* Wed Oct 22 2003 Vincent Danen <vdanen@mandrakesoft.com> 0.76-7mdks
- build with stack protection

* Sun Mar  9 2003 Paul Cox <paul@coxcentral.com> 0.76-6rph
- really 6rph (release wasn't changed)
- s/Copyright/License/

* Sat Feb  1 2003 Vincent Danen <vdanen@mandrakesoft.com> 0.76-6rph
- build for 9.1
- P0: errno.h fixes

* Fri Aug 09 2002 Vincent Danen <vdanen@mandrakesoft.com> 0.76-5rph
- build for 9.0

* Mon Apr 15 2002 Vincent Danen <vdanen@mandrakesoft.com> 0.76-4rph
- use new rph extension

* Mon Jan 14 2002 Vincent Danen <vdanen@mandrakesoft.com> 0.76-3mdk
- create /service (for compliance of djbdns and qmail)

* Thu Sep 27 2001 Vincent Danen <vdanen@mandrakesoft.com> 0.76-2mdk
- add packager tag

* Thu Sep  6 2001 Vincent Danen <vdanen@mandrakesoft.com> 0.76-1mdk
- 0.76
- remove patch to build under Mandrake 8.0 (included upstream)
- modified manpage package to add new manpages for pgrphack, readproctitle,
  and svscanboot
- include compatability links in /command

* Sat Oct 28 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.70-5mdk
- included patch to compile under Mandrake 8.0 from Thomas Mangin
  <systems-thomas@legend.co.uk>
- spec cleanups
- proper optimizations

* Sat Oct 28 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.70-4mdk
- more macros
- remove Packager tag

* Wed Jul 19 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.70-3mdk
- macroization
- cleanup spec

* Wed Apr 26 2000 Vincent Danen <vdanen@linux-mandrake.com> 0.70-2mdk
- fix group

* Wed Apr 26 2000 Vincent Danen <vdanen@linux-mandrake.com> 0.70-1mdk
- 0.70
- update specfile for spec-helper
- added URL
- new description

* Wed Feb 09 2000 Lenny Cartier <lenny@mandrakesoft.com>
- mandrake build
- bzip manpages

* Mon Apr 27 1998 Sergiusz Pawlowicz <ser@serek.arch.pwr.wroc.pl>
- first build for redhat-5.1, PGCC!
- added redhat.patch     
