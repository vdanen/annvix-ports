#
# spec file for ports package cvs2cl
#
# Ports Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments to the maintainer of this package:
#
#   vdanen@annvix.org
#
# $Id$

%define name		cvs2cl
%define version		2.51
%define release		3avx

%define _prefix		/usr/local
%define _mandir		/usr/local/share/man
%define _infodir	/usr/local/share/info
%define _sysconfdir	/usr/local/etc
%define _docdir		/usr/local/share/doc


Summary:	Generator of ChangeLog(s) from 'cvs log' output
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://www.red-bean.com/cvs2cl/cvs2cl.pl
Source1:	http://www.red-bean.com/cvs2cl/changelogs.html
License:	GPL
Group:		Development/Other
URL:		http://www.red-bean.com/cvs2cl/

BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildArch:	noarch

%description
CVS2CL attempt to product a nice ChangeLog from cvs log output, some
say nicer than rcs2log. He included with the OpenSouce cvs book :

http://cvsbook.red-bean.com/


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
install -m 0755 %{SOURCE0} %{buildroot}/%{_bindir}/%{name}
install -m 0644 %{SOURCE1} ./


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
rm -f changelogs.html


%files
%defattr(-,root,root)
%doc changelogs.html
%{_bindir}/%{name}


%changelog
* Wed Aug 03 2005 Vincent Danen <vdanen@opensls.org> 2.51-3avx
- Annvix ports

* Mon Dec 15 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.51-1mdk
- new release

* Sat Mar 22 2003 Lenny Cartier <lenny@mandrakesoft.com> 2.47-1mdk
- 2.47

* Fri Nov 29 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.44-1mdk
- 2.44
- updated url

* Tue Oct  2 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.38-2mdk
- Rebuild.

* Thu May  3 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.38-1mdk
- Add doc how to write changelog.
- 2.38.

* Thu Jul 27 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.10-1mdk
- First rpm pacakge


# end of file
