#
# spec file for ports package iptraf
#
# Ports Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments to the maintainer of this package:
#
#   ying@annvix.org
#
# $Id$

%define name		iptraf
%define version		2.7.0
%define release		1avx

%define _prefix		/usr/local
%define _mandir		/usr/local/share/man
%define _infodir	/usr/local/share/info
%define _sysconfdir	/usr/local/etc
%define _docdir		/usr/local/share/doc

Summary:	A console-based network monitoring utility
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
URL:		http://iptraf.seul.org/
Group:		Monitoring
Source:		ftp://ftp.cebu.mozcom.com/pub/linux/net/%{name}-%{version}.tar.gz
Patch0:		iptraf-2.7.0-install.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	ncurses-devel

%description
IPTraf is a console-based network monitoring utility.  IPTraf gathers
data like TCP connection packet and byte counts, interface statistics
and activity indicators, TCP/UDP traffic breakdowns, and LAN station
packet and byte counts.  IPTraf features include an IP traffic monitor
which shows TCP flag information, packet and byte counts, ICMP
details, OSPF packet types, and oversized IP packet warnings;
interface statistics showing IP, TCP, UDP, ICMP, non-IP and other IP
packet counts, IP checksum errors, interface activity and packet size
counts; a TCP and UDP service monitor showing counts of incoming and
outgoing packets for common TCP and UDP application ports, a LAN
statistics module that discovers active hosts and displays statistics
about their activity; TCP, UDP and other protocol display filters so
you can view just the traffic you want; logging; support for Ethernet,
FDDI, ISDN, SLIP, PPP, and loopback interfaces; and utilization of the
built-in raw socket interface of the Linux kernel, so it can be used
on a wide variety of supported network cards.


%prep
%setup -q 
%patch0 -p1 -b .instl


%build
# remove prebuilt cruft included in the tarball so that sparc and alpha can
# build properly
#rm -f src/{cfconv,iptraf,rvnamed}
make -C src CFLAGS="%{optflags}" \
    TARGET=%{_prefix}/sbin \
    LOCKDIR=/var/lock/subsys \
    LOGDIR=/var/log/iptraf \
    WORKDIR=/var/run/iptraf


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
install -d -m 0700 %{buildroot}/var/lock/iptraf
install -d -m 0700 %{buildroot}/var/log/iptraf
install -d %{buildroot}%{_prefix}/sbin
install -d %{buildroot}%{_mandir}/man8
install -m 0644 Documentation/*.8 %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}/var/run/iptraf

touch %{buildroot}/var/log/iptraf/rvnamed.log \
    %{buildroot}/var/run/iptraf/iptraf.cfg \
    %{buildroot}/var/run/iptraf/iptraf-promisclist.tmp \
    %{buildroot}/var/run/iptraf/iptraf-processcount.dat \
    %{buildroot}/var/run/iptraf/iptraf-itrafmoncount.dat

make -C src \
    TARGET=%{buildroot}%{_prefix}/sbin \
    LOCKDIR=%{buildroot}/var/lock/subsys \
    LOGDIR=%{buildroot}/var/log/iptraf \
    WORKDIR=%{buildroot}/var/run/iptraf \
    install


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc CHANGES FAQ LICENSE INSTALL README* RELEASE-NOTES
%doc Documentation
%attr(755,root,root) %{_prefix}/sbin/*
%{_mandir}/*/*
%dir %attr(700,root,root) /var/lock/iptraf
%dir %attr(700,root,root) /var/log/iptraf
%dir %attr(700,root,root) /var/run/iptraf
%config(missingok) /var/run/iptraf/iptraf.cfg
%config(missingok) /var/run/iptraf/iptraf-promisclist.tmp
%config(missingok) /var/run/iptraf/iptraf-processcount.dat
%config(missingok) /var/run/iptraf/iptraf-itrafmoncount.dat
%config(missingok) /var/log/iptraf/rvnamed.log


%changelog
* Mon Aug 15 2005 Vincent Danen <vdanen@annvix.org> 2.7.0-1avx
- first annvix ports submission from ying
- put iptraf in /usr/local/sbin not /usr/local/bin
- drop the RHized makefile patch; we don't need it

* Tue Jul 19 2005 Ying-Hung Chen <ying@annvix.org>
- rebuilt with annvix 1.0

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun 17 2003 Karsten Hopp <karsten@redhat.de> 2.7.0-8
- #97513, iptraf executable is 0700

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sat Dec 21 2002 Karsten Hopp <karsten@redhat.de>
- new URL
 
* Tue Nov 19 2002 Tim Powers <timp@redhat.com>
- rebuild on all arches

* Mon Jul 15 2002 Karsten Hopp <karsten@redhat.de> 2.7.0-3
- add missingok for /var/run/iptraf/ files (#68780)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jun 21 2002 Karsten Hopp <karsten@redhat.de> 2.7.0-1
- update to fix stale locks when IPTraf did not start due to an
  improper terminal size.
- this update adds support for wireless LAN interfaces (wlan*, wvlan*).

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Feb 22 2002 Karsten Hopp <karsten@redhat.de>
- build with gcc-3x

* Fri Feb 22 2002 Karsten Hopp <karsten@redhat.de>
- added missing define
- rebuild in new environment

* Wed Jan 23 2002 Karsten Hopp <karsten@redhat.de> (2.5.0-2)
- fix #55243 (unable to tag this process)

* Tue Jan 22 2002 Karsten Hopp <karsten@redhat.de>
- Update to 2.5.0

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jul 24 2001 Karsten Hopp <karsten@redhat.de>
- fix #49503 (BuildRequires)

* Sat Jul 07 2001 Karsten Hopp <karsten@redhat.de>
- Copyright -> License

* Mon May 28 2001 Karsten Hopp <karsten@redhat.de>
- really fix #42514

* Mon May 28 2001 Karsten Hopp <karsten@redhat.de>
- fix #42514 (executables had wrong permissions)

* Mon May 21 2001 Tim Powers <timp@redhat.com>
- updated to 2.4.0
- built for distro

* Mon Jan 22 2001 Karsten Hopp <karsten@redhat.de>
- update to 2.3.1 which fixes these bugs:
- segfault in IP Traffic Monitor
- segfault in promiscuous mode management
- failure of filters when source or dest is 255.255.255.255
- statistics logging bug
- small buffer overrun in TCP timeout log
- unrecognized IP display and filter code
- segfault bug when sorting an empty TCP window

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Thu Jul 13 2000 Karsten Hopp <karsten@redhat.de>
- rebuilt

* Wed Jun 28 2000 Karsten Hopp <karsten@redhat.de>
- fixed mandir
- changed install routine to allow building as non-root

* Mon May 15 2000 Tim Powers <timp@redhat.com>
- updated to 2.2.0

* Fri Nov 12 1999 Tim Powers <timp@redhat.com>
- updated to 2.1.0
- gzip man pages

* Wed Jul 28 1999 Tim Powers <timp@redhat.com>
- updated to version 2.0.2
- new patch added to that the spec file isn't out of control
  in the install section
- general spec cleanups
- built for 6.1

* Sat Apr 18 1999 Michael Maher <mike@redhat.com>
- built package for 6.0

* Sat Jan 16 1999 Anders Semb Hermansen <ahermans@vf.telia.no>
- Updated to version 1.4.2
- Used name and version variables in source field

* Wed Jan 6 1999 Anders Semb Hermansen <ahermans@vf.telia.no>
- Maintainer for RHCN: Anders Semb Hermansen
