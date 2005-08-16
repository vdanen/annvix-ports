#
# spec file for ports package ccache
#
# Ports Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments to the maintainer of this package:
#
#   ying@annvix.org
#
# $Id$

%define name		ccache
%define version		2.4
%define release		1avx

%define _prefix		/usr/local
%define _mandir		/usr/local/share/man
%define _infodir	/usr/local/share/info
%define _sysconfdir	/usr/local/etc
%define _docdir		/usr/local/share/doc

Summary:	Compiler cache
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
URL:		http://ccache.samba.org/
Group:		Development/Tools
Source:		http://ccache.samba.org/ftp/ccache/ccache-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires:	gcc, gcc-c++

%description
ccache is a compiler cache. It acts as a caching pre-processor to
C/C++ compilers, using the -E compiler switch and a hash to detect
when a compilation can be satisfied from cache. This often results in
a 5 to 10 times speedup in common compilations.


%prep
%setup
cat <<'EOF' >ccache.sh
if [ -x "%{_bindir}/ccache" -a -d "%{_libdir}/ccache/bin" ]; then
    if ! echo "$PATH" | grep -q %{_libdir}/ccache/bin; then
        PATH="%{_libdir}/ccache/bin:$PATH"
    fi
fi
EOF

cat <<'EOF' >ccache.csh
if ( "$path" !~ *%{_libdir}/ccache/bin* ) then
    set path = ( %{_libdir}/ccache/bin $path )
endif
EOF


%build
%configure
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall
install -Dp -m 0755 ccache.csh %{buildroot}%{_sysconfdir}/profile.d/ccache.csh
install -Dp -m 0755 ccache.sh %{buildroot}%{_sysconfdir}/profile.d/ccache.sh

install -d -m 0755 %{buildroot}%{_libdir}/ccache/bin/
for compiler in cc c++ gcc g++ gcc296 g++296; do
    ln -s -f %{_bindir}/ccache %{buildroot}%{_libdir}/ccache/bin/$compiler
done


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc README
%doc %{_mandir}/man?/*
%config %{_sysconfdir}/profile.d/*
%{_bindir}/*
%{_libdir}/ccache/


%changelog
* Mon Aug 15 2005 Vincent Danen <vdanen@annvix.org> 2.4-1avx

* Sat Jul 16 2005 Ying-Hung Chen <ying@annvix.org> - 2.4-1
- Repackage for Annvix.

* Wed Sep 22 2004 Dag Wieers <dag@wieers.com> - 2.4-1 #3053
- Updated to release 2.4.

* Sun Sep 28 2003 Dag Wieers <dag@wieers.com> - 2.3-0
- Updated to release 2.3.

* Sat May 10 2003 Dag Wieers <dag@wieers.com> - 2.2-1
- Fixed ccache.sh/ccache.csh. (Thomas Moschny)

* Sun May 04 2003 Dag Wieers <dag@wieers.com> - 2.2-0
- Initial package. (using DAR)
