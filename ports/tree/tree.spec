# $Id$

%define name	tree
%define version	1.4b3
%define release	3sls

%define _prefix		/usr/local
%define _mandir		/usr/local/share/man
%define _infodir	/usr/local/share/info
%define _sysconfdir	/usr/local/etc
%define _docdir		/usr/local/share/doc

Summary:	A utility which displays a tree view of directory contents.
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		File tools
License:	GPL
URL:		http://mama.indstate.edu/users/ice/tree/
Source:		ftp://mama.indstate.edu/linux/tree/%{name}-%{version}.tgz
Patch:		tree-typo.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
The tree utility recursively displays the contents of directories in a
tree-like format.  Tree is basically a UNIX port of the tree DOS
utility.

Install tree if you think it would be useful to view the contents of
specified directories in a tree-like format.

%prep
%setup -q -n %{name}-1.4
%patch -p1

%build
rm -f tree
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/{%{_bindir},%{_sbindir},%{_mandir}/man1}

make	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
	install

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_mandir}/man1/%{name}*
%doc README LICENSE CHANGES

%changelog
* Sat May 29 2004 Vincent Danen <vdanen@opensls.org> 1.4b3-3sls
- OpenSLS ports

* Mon Apr 19 2004 Michael Scherer <misc@mandrake.org> 1.4b3-2mdk 
- Birthday rebuild

* Wed Feb 26 2003 Aurelien Lemaire <alemaire@mandrakesoft.com> 1.4b3-1mdk
- New version 1.4b3
- Fix source path
- FIx patch file name

* Tue May 14 2002 Aurelien Lemaire <alemaire@mandrakesoft.com> 1.4b2-1mdk
- New version 1.4b2
- Patch updated for new manpage

* Mon Apr 15 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3-6mdk
- fix typo in manpage

* Wed Feb  6 2002 Aurelien Lemaire <alemaire@mandrakesoft.com> 1.3-5mdk
- rebuild release
- Add URL tag

* Sat Jul  7 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 1.3-4mdk
- remove hardcoded prefix
- reformat spec a bit

* Fri Jul 21 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3-3mdk
- macros, BM
- let spechelper compress man-pages

* Sat Jun 03 2000 Etienne Faure <etienne@mandrakesoft.com> 1.3-2mdk
- removed unused patch from sources
- Updated Source URL

* Tue Mar 14 2000 Daouda LO <daouda@mandrakesoft.com> 1.3-1mdk
- Adjust Group
- 1.3 

* Tue Nov 23 1999 Pixel <pixel@linux-mandrake.com>
- build release

* Fri Nov 12 1999 Damien Krotkine <damien@mandrakesoft.com>
- Mandrake release

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 6)

* Thu Dec 17 1998 Michael Maher <mike@redhat.com>
- built package for 6.0

* Mon Aug 10 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 29 1998 Cristian Gafton <gafton@redhat.com>
- installing in %{_bindir}

* Mon Oct 20 1997 Otto Hammersmith <otto@redhat.com>
- updated version
- fixed src url

* Fri Jul 18 1997 Erik Troan <ewt@redhat.com>
- built against glibc
