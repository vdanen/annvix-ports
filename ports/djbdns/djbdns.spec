#
# spec file for ports package djbdns
#
# Ports Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments to the maintainer of this package:
#
#   vdanen@annvix.org
#
# $Id$

%define name 		djbdns
%define version		1.05
%define release		24avx

%define _prefix		/usr/local
%define _mandir		/usr/local/share/man
%define _infodir	/usr/local/share/info
%define _sysconfdir	/usr/local/etc
%define _docdir		/usr/local/share/doc

Summary:	djbdns DNS server
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	D. J. Bernstein
Group:		System/Servers
URL:		http://cr.yp.to/djbdns.html
Source0:	http://cr.yp.to/djbdns/%{name}-%{version}.tar.gz
Source2:	tinydns-log.pl
Source3:	%{name}-getdata
Source4:	http://smarden.org/pape/djb/manpages/%{name}-%{version}-man.tar.gz
Source5:	tinydns.run
Source6:	tinydns-log.run
Source7:	axfrdns.run
Source8:	axfrdns-log.run
Source9:	dnscache.run
Source10:	dnscache-log.run
Source11:	dnscachex.run
Source12:	dnscachex-log.run
Source13:	tinydns.Makefile
Source14:	tinydns.rootdata
Patch0:		djbdns-1.05-errno.patch
# patches from http://homepages.tesco.net/~J.deBoynePollard/Softwares/djbdns/
Patch1:		tinydns-data-semantic-error.patch
Patch2:		dnscache-cname-handling.patch
Patch3:		tinydns-alias-chain-truncation.patch
Patch4:		dnsnamex.patch
Patch5:		dnscache-strict-forwardonly.patch
Patch6:		compiler-temporary-filename.patch
Patch7:		dnscacheip-space-separator.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildPreReq:	shadow-utils

Requires:	sh-utils, ipsvd, srv, rpm-helper
Conflicts:	bind, caching-nameserver

%description
djbdns is a collection of Domain Name System tools.  It includes several
components:

 * The dnscache program is a local DNS cache.  It accepts recursive DNS
   queries from local clients such as web browsers.  It collects responses
   from remote DNS servers.
 * The tinydns program is a fast, UDP-only DNS server.  It makes local DNS
   information available to the Internet.  It supports load balancing and
   client differentation.
 * The walldns program is a reverse DNS wall.  It provides matching reverse
   and forward records while hiding local host information.
 * The rbldns program is an IP-address-listing DNS server.  It uses DNS to
   publish a list of IP addresses, such as RBL or DUL.
 * The dns library handles outgoing and incoming DNS packets.  It can be
   used by clients such as web browsers to look up host addresses, hot names,
   MX records, etc.  It supports asynchronous resolution.
 * The dnsfilter program is a parallel IP-address-to-host-name converter.
 * The dnsip, dnsipq, dnsname, dnstxt, and dnsmx programs are simple
   command-line interfaces to DNS.
 * The dnsq and dnstrace programs are DNS debugging tools.

If you wish to replicate DNS information to secondary djbdns servers, you will
also need to install openssh and rsync to perform the actual replication.
This is not required unless you want to replicate to a secondary djbdns server
and is not required if your secondary is a BIND DNS server.


%package devel
Summary:	Development files for djbdns
Group:		Development/C
Requires:	%{name}

%description devel
These are header and library files for djbdns to be used in third-party 
programs.


%prep
%setup -q
# docs
# manpages
%setup -q -T -D -c -a 4 -n %{name}-%{version}

%patch0 -p1 -b .errno
%patch1 -p0 -b .semantic
%patch2 -p1 -b .query
%patch3 -p1 -b .alias-chain
%patch4 -p0 -b .dnsnamex
%patch5 -p1 -b .strict
%patch6 -p1 -b .compiler
%patch7 -p1 -b .cacheip

echo "gcc %{optflags}" >conf-cc
echo "gcc -s %{optflags}" >conf-ld
echo "%{_prefix}" >conf-home


%build
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}

make


%install
#make setup check
mkdir -p %{buildroot}{%{_sysconfdir},%{_bindir}}
install -m 0644 dnsroots.global %{buildroot}%{_sysconfdir}

for i in axfr-get axfrdns axfrdns-conf dnscache dnscache-conf dnsfilter \
    dnsip dnsipq dnsmx dnsname dnsq dnsqr dnstrace dnstracesort dnstxt pickdns \
    pickdns-conf pickdns-data pickdns-data random-ip rbldns rbldns-conf \
    rbldns-data tinydns tinydns-conf tinydns-data tinydns-edit tinydns-get \
    walldns walldns-conf
do
    install -m 0755 $i %{buildroot}%{_bindir}
done
install -m 0755 %{SOURCE3} %{buildroot}%{_bindir}

# manpages
mkdir -p %{buildroot}%{_mandir}/man{1,5,8}
install -m644 $RPM_BUILD_DIR/%{name}-%{version}/%{name}-man/*.1 %{buildroot}%{_mandir}/man1
install -m644 $RPM_BUILD_DIR/%{name}-%{version}/%{name}-man/*.5 %{buildroot}%{_mandir}/man5
install -m644 $RPM_BUILD_DIR/%{name}-%{version}/%{name}-man/*.8 %{buildroot}%{_mandir}/man8
cp $RPM_BUILD_DIR/%{name}-%{version}/%{name}-man/README \
    $RPM_BUILD_DIR/%{name}-%{version}/README.manpages

# install other extras
install -m 0755 %{SOURCE2} %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{_srvdir}/{dnscache,dnscachex,tinydns,axfrdns}/{log,peers}
mkdir -p %{buildroot}%{_srvlogdir}/{dnscache,dnscachex,tinydns,axfrdns}

install -m 0755 %{SOURCE5} %{buildroot}%{_srvdir}/tinydns/run
install -m 0755 %{SOURCE6} %{buildroot}%{_srvdir}/tinydns/log/run
install -m 0755 %{SOURCE7} %{buildroot}%{_srvdir}/axfrdns/run
install -m 0755 %{SOURCE8} %{buildroot}%{_srvdir}/axfrdns/log/run
install -m 0755 %{SOURCE9} %{buildroot}%{_srvdir}/dnscache/run
install -m 0755 %{SOURCE10} %{buildroot}%{_srvdir}/dnscache/log/run
install -m 0755 %{SOURCE11} %{buildroot}%{_srvdir}/dnscachex/run
install -m 0755 %{SOURCE12} %{buildroot}%{_srvdir}/dnscachex/log/run

mkdir %{buildroot}%{_srvdir}/tinydns/root
install -m 0644 %{SOURCE13} %{buildroot}%{_srvdir}/tinydns/root/Makefile
install -m 0644 %{SOURCE14} %{buildroot}%{_srvdir}/tinydns/root/data

# dnsroots.global is referenced via /etc, so make a symlink
mkdir -p %{buildroot}/etc
pushd %{buildroot}/etc
    ln -s ..%{_sysconfdir}/dnsroots.global .
popd

# devel files
mkdir -p %{buildroot}{%{_includedir}/djbdns,%{_libdir}/djbdns}
cp -av *.h %{buildroot}%{_includedir}/djbdns
cp -av *.a %{buildroot}%{_libdir}/djbdns


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
rm -rf $RPM_BUILD_DIR/%{name}-%{version}


%pre
%_pre_useradd tinydns %{_srvdir}/tinydns /bin/true 300
%_pre_useradd axfrdns %{_srvdir}/axfrdns /bin/true 301
%_pre_useradd dnscache %{_srvdir}/dnscache /bin/true 302

%post
if [ $1 = "1" ]; then
    if [ ! -d %{_srvdir}/tinydns/env ]; then
	# get IP address for eth0
	HOST=`/sbin/ifconfig eth0|grep 'inet addr'|gawk '{print $2}'|cut -d: -f2`
	# obtain a base (x.x.x)
	BASE=`/sbin/ifconfig eth0|grep 'inet addr'|gawk '{print $2}'|cut -d: -f2|cut -d. -f1,2,3`
	echo ""
	echo "Making some intelligent guesses on tinydns configuration, please check"
	echo "%{_srvdir}/tinydns to ensure configuration is correct."
	tmpdir="`mktemp -d /tmp/tinydns.XXXXXX`" && rm -rf $tmpdir
	%{_bindir}/tinydns-conf tinydns nobody $tmpdir $HOST
	cp -a $tmpdir/root/add* %{_srvdir}/tinydns/root/
	cp -a $tmpdir/env %{_srvdir}/tinydns/
	echo "%{_srvdir}/tinydns/root" >%{_srvdir}/tinydns/env/ROOT
	rm -rf $tmpdir
        touch %{_srvdir}/tinydns/peers/0
        chmod 644 %{_srvdir}/tinydns/peers/0
    fi

    if [ ! -d %{_srvdir}/axfrdns/env ]; then
	echo ""
	echo "Making some intelligent guesses on axfrdns configuration, please check"
	echo "%{_srvdir}/axfrdns to ensure configuration is correct."
	tmpdir="`mktemp -d /tmp/axfrdns.XXXXXX`" && rm -rf $tmpdir
	%{_bindir}/axfrdns-conf axfrdns nobody $tmpdir %{_srvdir}/tinydns $HOST
	cp -a $tmpdir/env %{_srvdir}/axfrdns/
	rm -rf $tmpdir
        touch %{_srvdir}/axfrdns/peers/0
        chmod 0 %{_srvdir}/axfrdns/peers/0
        echo "By default, zone transfers are not permitted.  You will need to modify the instructions"
        echo "directory %{_srvdir}/axfrdns/peers in order to allow hosts to obtain zone transfers."
        echo ""
	echo "Please modify %{_srvdir}/tinydns/root/Makefile to specify IP address of any"
	echo "secondary DNS servers you wish to replicate data to."
	echo ""
	echo "Post-install configuration completely.  Many guesses have been made to try to"
	echo "automate the setup as much as possible, however you will still need to"
	echo "fine-tune your configuration.  If you are converting to djbdns from BIND,"
	echo "please visit http://cr.yp.to/djbdns/frombind.html for further instrutions on"
	echo "how to do so."
    fi

    if [ ! -d %{_srvdir}/dnscachex/env ]; then
	# here we make a default configuration file if the service directory doesn't
	# already exist; as well, to keep things consistent, we install our own service
	# files first, so make dnscache-conf work on a temporary directory and then copy
	# the pertinent info out and into our real directory

	tmpdir="`mktemp -d /tmp/dnscachex.XXXXXX`" && rm -rf $tmpdir
        # get IP address for eth0
        HOST=`/sbin/ifconfig eth0|grep 'inet addr'|gawk '{print $2}'|cut -d: -f2`
        # obtain a base (x.x.x)
        BASE=`/sbin/ifconfig eth0|grep 'inet addr'|gawk '{print $2}'|cut -d: -f2|cut -d. -f1,2,3`
	echo "Configuring the external DNS caching service..."
        echo "Making some intelligent guesses on dnscache configuration, please check"
        echo "%{_srvdir}/dnscachex to ensure configuration is correct"
        %{_bindir}/dnscache-conf dnscache nobody $tmpdir $HOST
	cp -a $tmpdir/root %{_srvdir}/dnscachex/
	cp -a $tmpdir/env %{_srvdir}/dnscachex/
	cp -a $tmpdir/seed %{_srvdir}/dnscachex/
	rm -rf $tmpdir
	echo "%{_srvdir}/dnscachex/root" >%{_srvdir}/dnscachex/env/ROOT
        touch %{_srvdir}/dnscachex/root/ip/$BASE
        touch %{_srvdir}/dnscachex/peers/0
        chmod 644 %{_srvdir}/dnscachex/peers/0
    fi

    if [ ! -d %{_srvdir}/dnscache/env ]; then
	# now do the same for the local cache
	echo "Configuring the local DNS caching service..."
	echo "Making some intelligent guesses on dnscache configuration, please check"
	echo "%{_srvdir}/dnscache to ensure configuration is correct"
	tmpdir="`mktemp -d /tmp/dnscache.XXXXXX`" && rm -rf $tmpdir
	%{_bindir}/dnscache-conf dnscache nobody $tmpdir
	cp -a $tmpdir/root %{_srvdir}/dnscache/
	cp -a $tmpdir/env %{_srvdir}/dnscache/
	cp -a $tmpdir/seed %{_srvdir}/dnscache/
	echo "%{_srvdir}/dnscache/root" >%{_srvdir}/dnscache/env/ROOT
	rm -rf $tmpdir
        touch %{_srvdir}/dnscache/peers/{0,127.0.0.1}
        chmod 0 %{_srvdir}/dnscache/peers/0
        chmod 644 %{_srvdir}/dnscache/peers/127.0.0.1
    fi
fi

%_post_srv tinydns
%_post_srv axfrdns
%_post_srv dnscachex
%_post_srv dnscache


%preun
%_preun_srv tinydns
%_preun_srv axfrdns
%_preun_srv dnscachex
%_preun_srv dnscache


%postun
%_postun_userdel tinydns
%_postun_userdel axfrdns
%_postun_userdel dnscache


%files
%defattr(-,root,root)
%doc TINYDNS TODO CHANGES README README.manpages
%config(noreplace) %{_sysconfdir}/dnsroots.global
/etc/dnsroots.global
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%dir %{_srvdir}/tinydns
%dir %{_srvdir}/tinydns/root
%dir %{_srvdir}/tinydns/log
%dir %{_srvdir}/tinydns/peers
%{_srvdir}/tinydns/run
%config(noreplace) %{_srvdir}/tinydns/root/Makefile
%config(noreplace) %{_srvdir}/tinydns/root/data
%{_srvdir}/tinydns/log/run
%dir %attr(0750,logger,logger) %{_srvlogdir}/tinydns
%dir %{_srvdir}/axfrdns
%dir %{_srvdir}/axfrdns/log
%dir %{_srvdir}/axfrdns/peers
%{_srvdir}/axfrdns/run
%{_srvdir}/axfrdns/log/run
%dir %attr(0750,logger,logger) %{_srvlogdir}/axfrdns
%dir %{_srvdir}/dnscachex
%dir %{_srvdir}/dnscachex/log
%dir %{_srvdir}/dnscachex/peers
%{_srvdir}/dnscachex/run
%{_srvdir}/dnscachex/log/run
%dir %attr(0750,logger,logger) %{_srvlogdir}/dnscachex
%dir %{_srvdir}/dnscache
%dir %{_srvdir}/dnscache/log
%dir %{_srvdir}/dnscache/peers
%{_srvdir}/dnscache/run
%{_srvdir}/dnscache/log/run
%dir %attr(0750,logger,logger) %{_srvlogdir}/dnscache

%files devel
%defattr(-,root,root)
%dir %{_includedir}/djbdns
%{_includedir}/djbdns/*
%dir %{_libdir}/djbdns
%{_libdir}/djbdns/*


%changelog
* Wed Aug 03 2005 Vincent Danen <vdanen@annvix.org> 1.05-24avx
- spec cleanups for ports
- remove the html docs

* Mon May 09 2005 Vincent Danen <vdanen@annvix.org> 1.05-23avx
- fix ownership of log directories
- fix tinydns runscript... for some reason it doesn't like us
  setting the memory allocation on 64bit systems
- fix the tinydns Makefile

* Fri Apr 08 2005 Vincent Danen <vdanen@annvix.org> 1.05-22avx
- requires ipsvd
- drop requires on daemontools and ucspi-tcp
- update runscripts for tcpsvd and add the ./peers directory; post-config
  sets up tinydns and dnscachex without access restrictions, but axfrdns and
  dnscache are both restricted

* Sat Jul 17 2004 Vincent Danen <vdanen@annvix.org> 1.05-21avx
- Annvix build for ports
- rewmove all Mandrake-specific stuff
- remove initscript
- remove the localcache and extcache packages; everything is in one
  package now (makes sense when we're not using one "monolithic"
  initscript and since all the *cache files are already in djbdns proper
- remove the %%djbdir macro
- get rid of symlinks in /etc
- P1-P7: patches to fix various problems
- get rid of cronjob entry (no point in forcing my way of doing things on others)
- tinydns has static uid/gid 300
- axfrdns has static uid/gid 301
- dnscache has static uid/gid 302
- drop dnslog user and djbdns group

* Thu Jul  8 2004 Vincent Danen <vdanen@mandrakesoft.com> 1.05-20rph
- Mandrake 10 build
- patches from http://homepages.tesco.net/~J.deBoynePollard/Softwares/djbdns/

* Mon Mar 17 2003 Vincent Danen <vdanen@mandrakesoft.com> 1.05-19rph
- better build macros (automatically builds for the host OS)

* Sun Mar  9 2003 Paul Cox <paul@coxcentral.com> 1.05-18rph
- Patch0: errno fix for 9.1
- s/Copyright/License/

* Mon Apr 15 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.05-17rph
- 9.0 support
- add --with 8x to build for 8.x (builds for 9.0 by default)
- don't force a uid/gid number anymore; let the system assign it itself
- include RPMOPTIONS in README.RPM

* Mon Apr 15 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.05-16rph
- rebuild with rph extension

* Mon Jan 14 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.05-15mdk
- daemontools now includes /service, so we'll put symlinks in /service
  anyways (%%rootsrv is still useful if you want to change service location
  in the initscript)
- compatability in /etc (ugly, but we have to do it for the license)
- use %%_post_service and %%_preun_service if not %%build_72
- use /var/lock/subsys in initscript
- fix empty %%pre on non-7.2 builds

* Wed Dec 19 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.05-14mdk
- s/expend/expand/ (re: Oden Eriksson)
- add "it" to tinydns Makefile (now just "make it") (re: Oden Eriksson)

* Mon Nov 26 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.05-13mdk
- use --with 7.2 to build for 7.2; otherwise we build for 8.0+ which
  includes the required djbdns users
- use --with rootservice to use /service instead of /var/djbdns/service

* Fri Jun 20 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.05-12mdk
- rebuild for 8.0

* Sun Apr 29 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.05-11mdk
- fix initscript to use proper service directory

* Thu Apr 12 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.05-10mdk
- revamp package to provide local and external dnscache; external conflicts
  with full djbdns while local can co-exist with full djbdns
- on uninstall of djbdns-localcache, do not remove users if full djbdns is
  installed
- extcache uses dnscachex, localcache uses dnscache
- modified README.RPM
- djbdns-extcache and djbdns-localcache both obsolete djbdns-cache
- make sure all instance of /var/djbdns is replaced by %%{djbdir}
- because djbdns-cache is obsolete, you must first remove it (rpm -e) prior
  to installing extcache or localcache (otherwise the upgrade will seriously
  break (sorry about that, no real way around it))

* Thu Apr 12 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.05-9mdk
- fixes from Thomas Mangin <systems-thomas@legend.co.uk>:
  - fix typeo that resulted in damaged symlink
- suggestion from Thomas Mangin <systems-thomas@legend.co.uk>:
  - make initscript dynamic so rebuild with different service location does
    not require user to make manual changes to initscript

* Wed Apr 11 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.05-8mdk
- fix permissions on /var/djbdns/{tinydns,axfrdns,dnscachex}, force mode
  1755 so upgrades don't break logging

* Wed Apr 11 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.05-7mdk
- suggestion from Thomas Mangin <systems-thomas@legend.co.uk>:
  - make a define for location of the service directory (/service or
    /var/djbdns/service) so you can choose for rebuild (default is still
    /var/djbdns/service) 

* Sun Mar 25 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.05-6mdk
- modified %{djbdir}/tinydns/root/Makefile to not include comments (#) into
  the data file
- add daily cronjob
- include Kenji Rikitake's tinydns-log.pl, a logfile formatter for tinydns

* Sun Mar 25 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.05-5mdk
- fix initscript
- fix problem with uninstall scripts.  Users upgrading from 1.05-4mdk will
  need to remove djbdns-1.05-4mdk using the --noscripts command switch

* Wed Mar 14 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.05-4mdk
- don't turn djbdns off with chkconfig if upgrading
- create default %{djbdir}/tinydns/root/data file with instructions for
  secondary djbdns servers
- create djbdns-getdata which is used to obtain DNS info from BIND servers
  (useful when converting from BIND to djbdns)
- add build command to %{djbdir}/tinydns/root/Makefile so you can keep
  zone files in seperate files (ala BIND), but build them into the single
  data file djbdns needs (use: make build; make)
- added manpages from ftp.innominate.org

* Sun Mar 11 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.05-3mdk
- added devel package

* Sun Mar 11 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.05-2mdk
- the *-conf files will not operate if target directory exists, so remove
  the directory first, then run *-conf (not nice but necessary)
- run *-conf only on install, not upgrades
- add %%postun scripts to remove users/groups on uninstall
- fix symlinks
- make better test to see if djbdns is running on uninstall (prevent ugly
  error messages)
- include some of the DNS lookup tools in the djbdns-cache package
- update initscript to remove pid file on stop

* Sat Mar 10 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.05-1mdk
- first mandrake adaptation
- create initscript for djbdns
- create package for caching-only nameserver
- try to intelligently configure dnscache or tinydns and axfrdns (depending
  on the package installed)
- create symlinks for log files so they can all be reached under
  /var/log/djbdns instead of all over the place
