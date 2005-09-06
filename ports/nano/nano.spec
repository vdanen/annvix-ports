#
# spec file for ports package nano
#
# Ports Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments to the maintainer of this package:
#
#   spt@annvix.org
#
# $Id$

%define name 		nano
%define version         1.2.5
%define release		1avx

%define _prefix 	/usr/local
%define _bindir 	/usr/local/bin
%define _sysconfdir 	/usr/local/etc
%define _datadir 	/usr/local/share/
%define _mandir 	/usr/local/share/man
%define _infodir 	/usr/local/share/info
%define _docdir 	/usr/local/share/doc

Summary:	Nano's ANOther editor, an enhanced free Pico clone
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Editors
URL:		http://www.nano-editor.org
Source0:	http://www.nano-editor.org/dist/v1.2/%{name}-%{version}.tar.gz
BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires:       ncurses-devel

%description
GNU nano is a small and friendly text editor.  It aims to emulate the Pico
text editor while also offering a few enhancements.

%prep
%setup -q


%build
%configure
%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/locale
install -d %{buildroot}%{_mandir}/{man1,man5}
install -d %{buildroot}%{_infodir}

install -m 0755 nano %{buildroot}%{_bindir}

install -m 0644 nano.1 %{buildroot}%{_mandir}/man1/
install -m 0644 nanorc.5 %{buildroot}%{_mandir}/man5/
install -m 0644 nano.info %{buildroot}%{_infodir}

pushd po
    for i in `ls -1 *.gmo | cut -d. -f1` ;  do

	install -d %{buildroot}%{_datadir}/locale/$i/LC_MESSAGES/

        install -m 0644 $i.gmo %{buildroot}%{_datadir}/locale/$i/LC_MESSAGES/nano.mo
    done
popd


%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS BUGS COPYING ChangeLog INSTALL NEWS README THANKS TODO nanorc.sample
%{_bindir}/nano
%{_mandir}/*/*
%{_datadir}/locale/*/LC_MESSAGES/nano.mo
%{_infodir}/nano.info*


%changelog
* Sat Sep 03 2005 Sean P. Thomas <spt@annvix.org> 1.2.5-1avx
- initial port
