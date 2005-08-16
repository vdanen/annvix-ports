#
# spec file for ports package ying
#
# Ports Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments to the maintainer of this package:
#
#   ying@annvix.org
#
# $Id$

%define name		dos2unix
%define version		3.1
%define release		1avx

%define _prefix		/usr/local
%define _mandir		/usr/local/share/man
%define _infodir	/usr/local/share/info
%define _sysconfdir	/usr/local/etc
%define _docdir		/usr/local/share/doc

Summary:	Text file format converter
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Freely distributable
Group:		Applications/Text
Source:		%{name}-%{version}.tar.bz2
Patch0:		dos2unix-3.1.patch
Patch1:		dos2unix-3.1-segfault.patch
Patch2:		dos2unix-3.1-safeconv.patch
Patch3:		dos2unix-3.1-manpage-update-57507.patch
Patch4:		dos2unix-3.1-preserve-file-modes.patch
Patch5:		dos2unix-3.1-tmppath.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
Dos2unix converts DOS or MAC text files to UNIX format.


%prep
%setup -q
%patch0 -p1 -b .orig
%patch1 -p1 -b .segfault
%patch2 -p1 -b .safeconv
%patch3 -p1 -b .manpage-update-57507
%patch4 -p1 -b .preserve-file-modes
%patch5 -p1 -b .tmppath


for I in *.[ch]; do
    sed -e 's,#endif.*,#endif,g' -e 's,#else.*,#else,g' $I > $I.new
    mv -f $I.new $I
done


%build
make clean
make CFLAGS="%{optflags}"
make link


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_bindir},%{_mandir}/man1}
install -m 755 dos2unix %{buildroot}%{_bindir}
install -m 755 mac2unix %{buildroot}%{_bindir}
install -m 444 dos2unix.1 %{buildroot}%{_mandir}/man1
install -m 444 mac2unix.1 %{buildroot}%{_mandir}/man1


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root,0755)
%doc COPYRIGHT
%{_bindir}/dos2unix
%{_bindir}/mac2unix
%{_mandir}/*/*


%changelog
* Mon Aug 15 2005 Vincent Danen <vdanen@annvix.org> 3.1-1avx
- first commit to Annvix ports (for 1.1-CURRENT)
- spec cleanups

* Mon Aug  1 2005 Ying-Hung Chen <ying@annvix.org> 3.1-1avx
- Repackage for Annvix 1.0

* Wed Apr 13 2005 Tim Waugh <twaugh@redhat.com> 3.1-24
- Fixed tmppath patch (bug #150277).

* Thu Mar  3 2005 Mike A. Harris <mharris@redhat.com> 3.1-23
- Bump and rebuild for FC4, using gcc 4.

* Tue Feb  8 2005 Mike A. Harris <mharris@redhat.com> 3.1-22
- Bump and rebuild for FC4

* Wed Oct 20 2004 Miloslav Trmac <mitr@redhat.com> - 3.1-21
- Don't just delete the original file when destination and current directory
  are on different filesystems (#65548, #123069, patch by James Antill)
- Fix return type of StripDelimiter in dos2unix-3.1-safeconv.patch (#136148)

* Wed Oct  6 2004 Mike A. Harris <mharris@redhat.com> 3.1-20
- Added dos2unix-3.1-manpage-update-57507.patch to fix manpage (#57507)
- Added dos2unix-3.1-preserve-file-modes.patch to properly preserve file
  permissions (#91331,55183,112710,132145)

* Sun Sep 26 2004 Rik van Riel <riel@redhat.com> 3.1-19
- safer conversion w/ mac2unix (fix from bz #57508)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 05 2003 Elliot Lee <sopwith@redhat.com> 3.1-15
- Remove build dependency on perl, since perl BuildRequires: dos2unix,
  and there's no good reason not to just use sed here.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Oct  7 2002 Mike A. Harris <mharris@redhat.com> 3.1-13
- All-arch rebuild
- Added BuildRequires: perl

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Feb 28 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.1-10
- Build in new environment

* Thu Jan 17 2002 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix bug #57700 (segfault)
- Add the mac2unix symlink recommended in README
- Fix compiler warnings

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed Jan 10 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- shut up rpmlint

* Fri Nov 17 2000 Tim Powers <timp@redhat.com>
- use mkstemp instead of mktemp. Not much needed to change.

* Thu Nov 16 2000 Tim Powers <timp@redhat.com>
- cleaned up specfile a bit
- built for 7.1

* Tue Jul 07 1999 Peter Soos <sp@osb.hu> 
- Added Hungarian "Summary:" and "%description" 
- Corrected the file and directory attributes to rebuild the package 
  under RedHat Linux 6.0
