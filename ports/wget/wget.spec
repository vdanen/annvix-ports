#
# spec file for ports package wget
#
# Ports Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments to the maintainer of this package:
#
#   vdanen@annvix.org
#
# $Id$


%define name		wget
%define version		1.10
%define release		3avx

%define _prefix		/usr/local
%define _mandir		/usr/local/share/man
%define _infodir	/usr/local/share/info
%define _sysconfdir	/usr/local/etc
%define _docdir		/usr/local/share/doc


Summary: 	A utility for retrieving files using the HTTP or FTP protocols
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		Networking/WWW
URL: 		http://www.gnu.org/directory/GNU/wget.html
Source0:	http://ftp.gnu.org/gnu/wget/%{name}-%{version}.tar.gz
Patch0: 	wget-1.6-passive_ftp.patch
Patch1:		wget-1.7-remove-rpath-from-binary.patch
Patch2:		wget-1.8-no-solaris-md5.h.patch
Patch4:		wget-1.10-logstdout.patch
Patch5:		wget-1.9.1-suse-sanitize.patch

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildRequires:	gettext, openssl-devel, texinfo, autoconf2.5

Provides: 	webclient webfetch
Prereq: 	info-install


%description
GNU Wget is a file retrieval utility which can use either the HTTP or FTP
protocols. Wget features include the ability to work in the background
while you're logged out, recursive retrieval of directories, file name
wildcard matching, remote file timestamp storage and comparison, use of
Rest with FTP servers and Range with HTTP servers to retrieve files over
slow or unstable connections, support for Proxy servers, and
configurability.


%prep
%setup -q
%patch0 -p1 -b .passive_ftp
%patch1 -p1
%patch2 -p1 -b .md5
%patch4 -p1 -b .logstdout
%patch5 -p1 -b .can-2004-1487_1488


%build
#aclocal
autoconf
%configure2_5x
%make
# all tests must pass (but where are they?)
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

install -m 0755 util/rmold.pl %{buildroot}/%{_bindir}/rmold

%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info


%files -f %{name}.lang
%defattr(-,root,root,-)
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/wgetrc
%doc AUTHORS COPYING ChangeLog MAILING-LIST NEWS README TODO
%{_bindir}/*
%{_infodir}/*
%{_mandir}/man1/wget.1*


%changelog
* Sun Sep 11 2005 Vincent Danen <vdanen@annvix.org> 1.10-3avx
- move to ports; nothing requires wget
- drop P3 because wgetrc is in fact now in /usr/local/etc

* Thu Aug 11 2005 Vincent Danen <vdanen@annvix.org> 1.10-2avx
- bootstrap build (new gcc, new glibc)

* Mon Jul 04 2005 Vincent Danen <vdanen@annvix.org> 1.10-1avx
- 1.10
- drop P1, P6, P7, P10, P11, P12, P13 (non-essential)
- rediff P7, P9
- renumber patches

* Thu Jun 09 2005 Vincent Danen <vdanen@annvix.org> 1.9.1-3avx
- P14: patch from SUSE to fix CAN-2004-1487 and CAN-2004-1488

* Wed Dec 22 2004 Vincent Danen <vdanen@annvix.org> 1.9.1-2avx
- P13: fix large file support (mdk anthill #1166)

* Tue Aug 17 2004 Vincent Danen <vdanen@annvix.org> 1.9.1-1avx
- 1.9.1
- remove P5, P8 (upstream)
- updated P1, P7, P11 (from mandrake)
- BuildRequires: autoconf2.5
- P12: fix utf8 encoding on console with de locale (#6597, Abel Cheung)
  (tvignaud)
- get rid of old chinese translation (deaddog)
- %%configure2_5x, %%makeinstall_std (deaddog)

* Fri Jun 18 2004 Vincent Danen <vdanen@annvix.org> 1.8.2-15avx
- require info-install, not the file
- Annvix build

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 1.8.2-14sls
- minor spec cleanups

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 1.8.2-13sls
- OpenSLS build
- tidy spec

* Sat Sep 06 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.8.2-12mdk
- fix wrong french translation (#4915)

* Tue Jul 22 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.8.2-11mdk
- rebuild
- rm -rf %{buildroot} at the beginning of %%install

* Thu Jun 05 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.8.2-10mdk
- patch 10: support correct spelling of '--referrer' in options (#3991)
  (from Wes Landaker, hand edited by me so that patch succeed in applying it)

* Tue Feb 11 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.8.2-9mdk
- enable parallel build

* Wed Jan 22 2003 François Pons <fpons@mandrakesoft.com> 1.8.2-8mdk
- created patch so that -o - allow log to stdout.

* Wed Jan 15 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.8.2-7mdk
- Rebuild again agains latest SSL.

* Tue Jan 14 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.8.2-6mdk
- Sync with latest OpenSSL.

* Thu Jan 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.8.2-5mdk
- build release

* Wed Dec 11 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.8.2-4mdk
- fix url (yura gusev)

* Tue Dec 10 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.8.2-3mdk
- P8: security fix for directory traversal problem
- remove double %%{_mandir} entry in %%files

* Wed Sep 04 2002 François Pons <fpons@mandrakesoft.com> 1.8.2-2mdk
- created patch 7 to allow @ in url password.

* Sun Jul 07 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.8.2-1mdk
- Bump!
- Run make check in build.
- Patch cleanup and remove applied patches.

* Thu Jun  6 2002 Stefan van der Eijk <stefan@eijk.nu> 1.8.1-4mdk
- BuildRequires
- fixed %%configure

* Tue Apr 16 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.8.1-3mdk
- config file is in /etc, not in /usr/local [Patch10]
- warns of passwords in process list [Patch11]
- let DO_REALLOC_FROM_ALLOCA from wget.h work [Patch12]
- fix handling of <meta http-equiv=Refresh> (without "a content") [Patch13]
- fix .netrc parsing [Patch14]
- fix quotations of : and @ in username and password [Patch15]

* Thu Dec 27 2001 Stew Benedict <sbenedict@mandrakesoft.com> 1.8.1-2mdk
- drop PPC segfault patch

* Thu Dec 27 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.8.1-1mdk
- Wget 1.8.1 (Abel).

* Wed Dec 19 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.8-1mdk
- The all-new-ad-shiny 1.8 out for download.
- Don't use /usr/include/md5.h but /usr/include/openssl/md5.h.

* Wed Nov 28 2001 François Pons <fpons@mandrakesoft.com> 1.7.1-3mdk
- added provides to webfetch (used by urpmi).

* Tue Nov 27 2001 Stew Benedict <sbenedict@mandrakesoft.com> 1.7.1-2mdk
- remove rpath, patch core dump on long URL - PPC

* Wed Nov 21 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.7.1-1mdk
- Make a shiny 1.7.1 for the cooker folks.

* Thu Jul 05 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.7-2mdk
- gcc accepts "-R" argument instead of "-rpath". Let configure determine
  the fact intself, hence properly enabling SSL. (patch4).
- Add missing manpage
- BuildRequires: libopenssl0-devel

* Wed Jun 06 2001 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.7-1mdk
- removed obsolete patches
- added patch 3
- Geoffrey Lee <snailtalk@mandrakesoft.com>
  - Remove Abel's translation, seems to have been integrated in wget already.
  
* Thu Apr 12 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.6-7mdk
- Add an updated Big5 translation from Abel Cheung (maddog@linuxhall.org).

* Tue Apr 10 2001 François Pons <fpons@mandrakesoft.com> 1.6-6mdk
- made --passive-ftp on by default.

* Tue Mar 27 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.6-5mdk
- Make a patch for a missing setlocale() call (Andrew Lee, YCheng).

* Sat Mar 03 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.6-4mdk
- Port SSL patch to 1.6 and activate it (please let me know if you found
  problems and no to the maintainner).

* Sun Jan 28 2001 Geoffrey Lee <snailtalk@mandrakesoft.co> 1.6-3mdk
- remove bogus zh locale.
 
* Sun Jan 28 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.6-2mdk
- put in Chinese locales.

* Wed Jan 03 2001 David BAUDENS <baudens@mandrakesoft.com> 1.6-1mdk
- 1.6
- Spec clean up

* Fri Dec  8 2000  Daouda Lo <daouda@mandrakesoft.com> 1.5.3-13mdk
- bug fix (rfc 1738 reserves some character for special meaning) thanx Anon
- remove duplicate description

* Wed Jul 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5.3-12mdk
- BM

* Wed Jul 12 2000 Christian Zoffoli <czoffoli@linux-mandrake.com> 1.5.3-11mdk
- removed %group
- removed _sysconfdir 

* Tue Jul 11 2000 Christian Zoffoli <czoffoli@linux-mandrake.com> 1.5.3-10mdk
- macroszifications

* Sun Jul 02 2000 Christian Zoffoli <czoffoli@linux-mandrake.com> 1.5.3-9mdk.ipv6
- IPv6 support
- Merge with PLD distro

* Fri May 19 2000 Jerome Martin <jerome@mandrakesoft.com> 1.5.3-9mdk
- rebuilded package to fix distribution tag

* Wed Apr  5 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 1.5.3-8mdk
- updated BuildRoot
- new group Networking/WWW
- new home URL for source tarball

* Sun Nov  7 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- don't permit chmod 777 on symlinks.

* Wed Jul 21 1999 Gregus <gregus@etudiant.net>
- fr locale

* Wed May  5 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Fri Dec 18 1998 Bill Nottingham <notting@redhat.com>
- build for 6.0 tree
- add Provides

* Sat Oct 10 1998 Cristian Gafton <gafton@redhat.com>
- strip binaries
- version 1.5.3

* Sat Jun 27 1998 Jeff Johnson <jbj@redhat.com>
- updated to 1.5.2
* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- modified group to Applications/Networking

* Wed Apr 22 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.5.0
- they removed the man page from the distribution (Duh!) and I added it back
  from 1.4.5. Hey, removing the man page is DUMB!

* Fri Nov 14 1997 Cristian Gafton <gafton@redhat.com>
- first build against glibc
