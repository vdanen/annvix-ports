%define name	joe
%define version	3.0
%define release	2sls

%define _prefix	/usr/local
%define _mandir /usr/local/share/man
%define _infodir /usr/local/share/info
%define _sysconfdir /usr/local/etc

Summary:	An easy to use, modeless text editor
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
URL:		http://sourceforge.net/projects/joe-editor
Group:		Editors
Source:		http://heanet.dl.sourceforge.net/sourceforge/joe-editor/%{name}-%{version}.tar.gz
Patch1:		joe-2.9.8-gnoterm.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	ncurses-devel

%description 
Joe is an easy to use, modeless text editor which would be very
appropriate for novices.  Joe uses the same WordStar keybindings used
in Borland's development environment.

You should install joe if you've used it before and you liked it, or
if you're still deciding what text editor you'd like to use, or if you
have a fondness for WordStar.  If you're just starting out, you should
probably install joe because it is very easy to use.

%prep
%setup -q
%patch1 -p1 -b .gnoterm

%build
export CFLAGS="$RPM_OPT_FLAGS -DUSE_LOCALE"
%configure2_5x
%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall transform=''

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr (-,root,root)
%{_bindir}/*
%dir %{_sysconfdir}/joe 
%config(noreplace) %{_sysconfdir}/joe/*
%{_mandir}/man1/*

%changelog
* Fri May 28 2004 Vincent Danen <vdanen@opensls.org> 3.0-2sls
- don't set sysconfdir to sysconfdir/joe or we end up with
  /usr/local/etc/joe/joe

* Fri May 28 2004 Vincent Danen <vdanen@opensls.org> 3.0-1sls
- OpenSLS ports

* Mon Apr 26 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.0-1mdk
- Release: 3.0.
- Removed Patch0.

* Sat Feb 07 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.9.8-2mdk
- Merged gnome term patches from RH (Patch1).
- Renamed Patch2 -> Patch0.

* Tue Aug 19 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.9.8-1mdk
- Release: 2.9.8.
- Removed Patch0 (bound), merged in main.
- Removed Patch1 (help), merged in main.
- Upgraded Patch2 (zerorc), sync with RH version.
- Removed Patch3 (restricted), merged in main.
- Removed Patch4, Patch5, no longer needed.
- Use %%configure2_5x.

* Wed Jul 16 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2.9.7-8mdk
- fix gcc-3.3 build (P5)

* Mon Jan 20 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.9.7-7mdk
- Patch0-4 merged from RH.

* Tue Aug 13 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.9.7-6mdk
- Rebuilt.

* Tue Jan 22 2002 David BAUDENS <baudens@mandrakesoft.com> 2.9.7-5mdk
- Fix menu entry (icon).

* Wed Jan 16 2002 David BAUDENS <baudens@mandrakesoft.com> 2.9.7-4mdk
- Clean after build.

* Mon Jan 11 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.9.7-3mdk
- fixed changelog (macro expansion ;-p).

* Mon Jan 11 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.9.7-2mdk
- added transform='' to %%makeinstall to avoid
  %%{arch}-joe and %%{arch}-termidx names in /usr/bin.

* Mon Jan 11 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.9.7-1mdk
- updated to version 2.9.7 final.

* Sat Jul 14 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.9.7-0.1mdk
- updated to version 2.9.7pre0.

* Tue May  8 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 2.9.6-1mdk
- version 2.9.6
- clean specfile

* Sat Mar 31 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.9.5-1mdk
- After 6 years a new release...

* Tue Mar  6 2001 Vincent Danen <vdanen@mandrakesoft.com> 2.8-23mdk
- security fix: don't use .joerc in CWD, just ~/.joerc and /etc/joe/joerc

* Wed Nov 22 2000 Vincent Danen <vdanen@mandrakesoft.com> 2.8-22mdk
- security fix: don't blindly write to DEADJOE, unlink it and
  create it safely first

* Mon Sep 25 2000 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.8-21mdk
- sync with latest RedHat patches (procrc)
- removed patch7 (included into joe-resize2.patch) and patch10
  (same things into joe-vfile.patch).

* Mon Sep 25 2000 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.8-20mdk
- fixed a typo in menu.
- included macro and BM fixes to SPEC file from Stefan van der
  Eijk <s.vandereijk@chello.nl>.

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.8-19mdk
- automatically added BuildRequires

* Fri Apr 28 2000 Vincent Saugey <vince@mandrakesoft.com> 2.8-18mdk
- add three size of icons

* Thu Apr 13 2000 Vincent Saugey <vince@mandrakesoft.com> 2.8-17mdk
- Add menu entry
- Corrected group
- Remove strip and bzip2 in spec file

* Fri Feb 04 2000 Giuseppe Ghibò <ghibo@linux-mandrake.com>
- merged with Bero's patch from Has de Goede <hans@highrise.nl> to fix the
  End Key.

* Fri Jan 28 2000 Francis Galiegue <francis@mandrakesoft.com> 2.8-15mdk
- Added missing %defattr() in %files section.

* Sat Dec 18 1999 Giuseppe Ghibò <ghibo@linux-mandrake.com>
- merged with latest Chris Gafton <gafton@redhat.com> patches
  (joe-2.8-security and joe-2.8-deadjoe).
- finally fixed a bug causing segfault on big files with short
  name (joe-2.8-vsmk).

* Thu Dec 02 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- Build release for Oxygen
- fix sucks on locale patch where -p1 delete the _filename_ ...

* Wed Aug 26 1999 Giuseppe Ghibò <ghibo@linux-mandrake.com>
- fixed a bug causing segfault on long filenames.

* Fri Jun 04 1999 Giuseppe Ghibò <ghibo@caesar.polito.it>
- added patch to get joe working on terminals supporting
  ti/te entries.

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Fri Apr 09 1999 Cristian Gafton <gafton@redhat.com>
- added locale patch from  Petr Kolar <PETR.KOLAR@vslib.cz>
  (yeah, finally!)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 17)

* Wed Jan 20 1999 Alex deVries <puffin@redhat.com>
- added mipseb support

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Tue Sep 15 1998 Cristian Gafton <gafton@redhat.com>
- built with Alan's -port patch

* Fri May 08 1998 Cristian Gafton <gafton@redhat.com>
- enable -asis in the config files so international keyboards will be better
  supported

* Fri May 01 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri May 01 1998 Cristian Gafton <gafton@redhat.com>
- /usr/lib/joe/* are config files

* Thu Apr 09 1998 Cristian Gafton <gafton@redhat.com>
- manhattan build

* Thu Dec 11 1997 Cristian Gafton <gafton@redhat.com>
- fixed termcap problems for terms other than 80x25
- added support for buildroot and BuildRoot

* Mon Jul 21 1997 Erik Troan <ewt@redhat.com>
- built against glibc
