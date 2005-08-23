#
# spec file for ports package dot-forward
#
# Ports Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments to the maintainer of this package:
#
#   vdanen@annvix.org
#
# $Id$


%define name		dot-forward
%define version		0.71
%define release		6avx

%define _prefix		/usr/local
%define _mandir		/usr/local/share/man
%define _infodir	/usr/local/share/info
%define _sysconfdir	/usr/local/etc
%define _docdir		/usr/local/share/doc


Summary:	.forward handler for qmail
Name:		%{name}
Version:	%{version}
Release:	%{release}
Copyright:	D. J. Bernstein
Group:		System/Servers
URL:		http://cr.yp.to/dot-forward.html
Source0:	http://cr.yp.to/software/%{name}-%{version}.tar.gz
Patch0:		dot-forward-0.71-errno.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
dot-forward reads sendmail's .forward files under qmail.


%prep
%setup -q
%patch0 -p1 -b .errno


%build
CFLAGS="%{optflags}"
make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_bindir},%{_mandir}/man1}

install -m 0755 dot-forward %{buildroot}%{_bindir}	
install -m 0644 dot-forward.1 %{buildroot}%{_mandir}/man1


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
rm -rf $RPM_BUILD_DIR/%{name}-%{version}


%files
%defattr (-,root,root)
%doc BLURB CHANGES README TODO INSTALL
%{_bindir}/dot-forward
%{_mandir}/man1/dot-forward.1*


%changelog
* Tue Aug 23 2005 Vincent Danen <vdanen@mandrakesoft.com> 0.71-6avx
- Annvix ports

* Sat Feb  1 2003 Vincent Danen <vdanen@mandrakesoft.com> 0.71-5rph
- build for 9.1
- P0: fix errno.h errors

* Fri Aug  9 2002 Vincent Danen <vdanen@mandrakesoft.com> 0.71-4rph
- build for 9.0

* Mon Apr 15 2002 Vincent Danen <vdanen@mandrakesoft.com> 0.71-3rph
- use new rph extension

* Thu Sep 27 2001 Vincent Danen <vdanen@mandrakesoft.com> 0.71-2mdk
- add packager tag

* Sun Feb 18 2001 Vincent Danen <vdanen@mandrakesoft.com> 0.71-1mdk
- 0.71

* Thu Jul 27 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.51-2mdk
- macroization

* Mon Jul 17 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.51-1mdk
- mandrake build
