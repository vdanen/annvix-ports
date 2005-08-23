#
# spec file for ports package qmail
#
# Ports Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments to the maintainer of this package:
#
#   vdanen@annvix.org
#
# $Id$
#
### This RPM must be built as root or on a system where the qmail users
### already exist.  On 8.[12] the qmail users are pre-installed, on all
### others you must have qmail installed or create the qmail users prior to
### building the package (the rpm will attempt to do this if the users are not
### found which is why it must be built as root in this case; or you need to
### have sudo access to group{add,del} and user{add,del}


%define name		qmail
%define version		1.03
%define release		26avx
%define qdir		/var/qmail
%define sauthver	0.31
%define ldapver		20011001a
%define tlsver		20020801

# User-definable configuration items:

%define rootcmd /usr/bin/sudo
%define useradd /usr/sbin/useradd
%define userdel /usr/sbin/userdel
%define groupadd /usr/sbin/groupadd
%define groupdel /usr/sbin/groupdel

%define build_qmailqueue 0
%define build_tls 0
%define build_linksync 0
%define build_smtpauth 0
# Build without CRAM-MD5 support; only checked if smtpauth is used
%define build_nocrammd5 0
%define build_ldap 0
%define build_dietlibc 0
%define build_msglog 0

# commandline overrides:
# rpm -ba|--rebuild --with 'xxx'
%{?_with_qmailqueue: %{expand: %%define build_qmailqueue 1}}
%{?_with_tls: %{expand: %%define build_tls 1}}
%{?_with_linksync: %{expand: %%define build_linksync 1}}
%{?_with_smtpauth: %{expand: %%define build_smtpauth 1}}
%{?_with_nocrammd5: %{expand: %%define build_nocrammd5 1}}
%{?_with_ldap: %{expand: %%define build_ldap 1}}
%{?_with_dietlibc: %{expand: %%define build_dietlibc 1}}
%{?_with_msglog: %{expand: %%define build_msglog 1}}

# do some checks; can't build with both TLS and smtp-auth, or TLS and LDAP
# so we make TLS the lesser priority and turn it off if defined with the
# others
%if %{build_smtpauth}
%define build_tls 0
%endif
%if %{build_ldap}
%define build_tls 0
%endif

%if %{build_dietlibc}
%define confcc diet gcc
%else
%define confcc gcc
%endif

Summary:	qmail Mail Transfer Agent
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	D. J. Bernstein
Group:		System/Servers
URL:		http://www.qmail.org/
Source0:	http://cr.yp.to/software/%{name}-%{version}.tar.gz
Source1:	dot.qmail-msglog
Source2:	cron.hourly
Source3:	qmail.rc
Source4:	qmail.init
Source5:	qmail-install.sh
Source6:	qmail-pop3d.run
Source7:	qmail-pop3d-log.run
Source8:	qmail-send.run
Source9:	qmail-send-log.run
Source10:	qmail-smtpd.run
Source11:	qmail-smtpd-log.run
Source12:	qmail-qmqpd.run
Source13:	qmail-qmqpd-log.run
Source14:	README.patches.bz2
Source15:	qmail-qmtpd.run
Source16:	qmail-qmtpd-log.run

# sources required for extra functionality (not used by default)
Source100:	http://members.elysium.pl/brush/qmail-smtpd-auth/dist/qmail-smtpd-auth-%{sauthver}.tar.gz

# These patches are not included by default; they must be enabled on the
# command line when rebuilding.  See README.patches for more info.
Patch0:		qmailqueue-patch
Patch1:		qmail-1.03-tls-%{tlsver}.patch
Patch2:		qmail-1.03-link-sync.patch
Patch3:		qmail-ldap-1.03-%{ldapver}.patch

# Patches that can be applied
Patch100:	qmail-1.03-queue_extra.patch
Patch101:	qmail-1.03-errno.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	shadow-utils
%if %{build_tls}
BuildRequires:	openssl-devel >= 0.9.6a
%endif
%if %{build_ldap}
BuildRequires:	libldap2-devel
Requires:	libldap2
%endif
%if %{build_dietlibc}
BuildRequires:	dietlibc = 0.28
%endif

Requires:	chkconfig, initscripts, sh-utils, daemontools, ucspi-tcp
%if %{build_tls}
Requires:	openssl >= 0.9.6a
%endif
%if %{build_smtpauth} && !%{build_nocrammd5}
Requires:	cmd5checkpw
%endif
Conflicts:	sendmail exim smail postfix
Provides:	smtpdaemon MTA


%description
qmail is a small, fast, secure replacement for the sendmail package, which is 
the program that actually receives, routes, and delivers electronic mail.  

*** Note: Be sure and read the documentation as there are some small but very 
significant differences between sendmail and qmail and the programs that 
interact with them.

The file README.patches in the documentation directory contains important
information on rebuilding qmail with various patches such as the qmailqueue
patch, TLS support in qmail, etc.  The file README.RPM in the documentation
directory contains additional information about how this particular qmail
package was built.

You can also rebuild qmail with some optional patches and enhancements.  The
following are valid build options (ie. use with --rebuild):

  --with qmailqueue	Use the qmailqueue patch
  --with tls		Use the TLS patch
  --with linksync	Use the linksync patch
  --with smtpauth	Use the SMTP-AUTH patch
  --with nocrammd5	Don't use CRAM-MD5 support with the SMTP-AUTH patch
  --with ldap		Use the LDAP patch
  --with dietlibc	Build with dietlibc
  --with msglog		Allow the use of alias/.qmail-msglog

Please note that the dietlibc support is *very* experimental.


%package pop3d
Summary:	POP3 daemon for qmail
Group:		System/Servers
Requires:	%{name} = %{version}, checkpassword

%description pop3d
The qmail-pop3d packages provides POP3 support for qmail mail servers.  If 
you need to be able to use POP3 with your qmail server, you should install 
this package.


%package qmqpd
Summary:	qmqp support for qmail
Group:		System/Servers
Requires:	%{name} = %{version}

%description qmqpd
The qmail-qmqpd packages provides QMQP (Quick Mail Queueing Protocol)
support for qmail mail servers.  If you need qmail to receive mail via QMQP,
you should install this package.


%prep
### setup README.RPM: -----------------------------------------------------

COMPILER="Compiler:               $(gcc -v 2>& 1|tail -1)"
HARDWARE="Hardware platform:      $(uname -m)"
%if %{build_dietlibc}
LIBRARY="Library:                $(rpm -q dietlibc)"
%else
LIBRARY="Library:                $(rpm -q glibc)"
%endif
OSVERSION="Linux Kernel:           $(uname -sr)"
PACKAGER="Packager:               %{packager}"
AVXRELEASE="Annvix release:       $(cat /etc/annvix-release)"
RPMVERSION="RPM Version:            $(rpm -q rpm)"
RPMOPTIONS="Package build options: "

%setup -q

%if %{build_smtpauth}
#FIXME: make me unarchive directly to qmail-1.03/ and not subdirs
%setup -q -n %{name}-%{version} -D -T -a100
%endif

%patch101 -p1 -b .errno
### optional patches ------------------------------------------------------
%if %{build_qmailqueue}
%patch0 -p1 -b .qmailqueue
RPMOPTIONS="$RPMOPTIONS qmailqueue"
%endif
%if %{build_tls}
%patch1 -p1 -b .tls
RPMOPTIONS="$RPMOPTIONS tls"
%endif
%if %{build_linksync}
%patch2 -p0 -b .linksync
RPMOPTIONS="$RPMOPTIONS linksync"
%endif
%if %{build_msglog}
# enable QUEUE_EXTRA
%patch100 -p1 -b .queue_extra
RPMOPTIONS="$RPMOPTIONS msglog"
%endif
%if %{build_ldap}
%patch3 -p1 -b .ldap
RPMOPTIONS="$RPMOPTIONS ldap"
# add -lresolv
perl -pi -e 's/LDAPLIBS=-L\/usr\/local\/lib -lldap -llber/LDAPLIBS=-L\/usr\/local\/lib -lldap -llber -lresolv/g' $RPM_BUILD_DIR/%{name}-%{version}/Makefile
%endif

%if %{build_smtpauth}
( mv qmail-smtpd-auth-%{sauthver}/* .; patch -p0 < auth.patch )
RPMOPTIONS="$RPMOPTIONS smtpauth"
%%if %{build_nocrammd5}
# Remove CRAM-MD5 support
perl -pi -e 's|^#define\s+AUTHCRAM|#undef AUTHCRAM|' qmail-smtpd.c
RPMOPTIONS="$RPMOPTIONS without cram-md5"
%%endif
%endif

%if %{build_dietlibc}
RPMOPTIONS="$RPMOPTIONS dietlibc"
%endif

### make README.RPM -------------------------------------------------------
cat <<EOF >>$RPM_BUILD_DIR/%{name}-%{version}/README.RPM
The qmail rpm packages were created in the following build environment:

$AVXRELEASE
$HARDWARE
$OSVERSION
$LIBRARY
$COMPILER
$RPMVERSION
$PACKAGER
$RPMOPTIONS

Ever effort has been made to ensure that the package behaves correctly and
as the author intended.
EOF

bunzip2 -k %{SOURCE14} -c > $RPM_BUILD_DIR/%{name}-%{version}/README.patches

### set compiler options --------------------------------------------------
%if %{build_tls}
    echo "%{confcc} %{optflags} -DTLS -I/usr/include/openssl" >conf-cc
%else
    echo "%{confcc} %{optflags}" >conf-cc
%endif

%if %{build_dietlibc}
    echo "%{confcc} %{optflags} -static -s" >conf-ld
%else
    echo "%{confcc} -s %{optflags}" >conf-ld
%endif


%build
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}

### cleanup any lingering tempfiles ---------------------------------------
rm -f %{_tmppath}/{{qmail,nofiles}-g,alias-u,qmail{d,l,p,q,r,s}-u}

### create groups and users -----------------------------------------------
# unfortunately we cannot get around this as the qmail installer craps out
# if the groups/users are not available (stupid)
grep "^qmail:" /etc/group >/dev/null || touch %{_tmppath}/qmail-g
if [ -f %{_tmppath}/qmail-g ]; then
    %{rootcmd} %{groupadd} -r -g 400 qmail
fi
grep "^nofiles:" /etc/group >/dev/null || touch %{_tmppath}/nofiles-g
if [ -f %{_tmppath}/nofiles-g ]; then
    %{rootcmd} %{groupadd} -r -g 401 nofiles
fi
grep "^alias:" /etc/passwd >/dev/null || touch %{_tmppath}/alias-u
if [ -f %{_tmppath}/alias-u ]; then
    %{rootcmd} %{useradd} -d %{qdir}/alias -g 401 -u 400 -M -r -s /bin/true alias
fi
grep "^qmaild:" /etc/passwd >/dev/null || touch %{_tmppath}/qmaild-u
if [ -f %{_tmppath}/qmaild-u ]; then
    %{rootcmd} %{useradd} -d %{qdir} -g 401 -u 401 -M -r -s /bin/true qmaild
fi
grep "^qmaill:" /etc/passwd >/dev/null || touch %{_tmppath}/qmaill-u
if [ -f %{_tmppath}/qmaill-u ]; then
    %{rootcmd} %{useradd} -d %{qdir} -g 401 -u 402 -M -r -s /bin/true qmaill
fi
grep "^qmailp:" /etc/passwd >/dev/null || touch %{_tmppath}/qmailp-u
if [ -f %{_tmppath}/qmailp-u ]; then
    %{rootcmd} %{useradd} -d %{qdir} -g 401 -u 403 -M -r -s /bin/true qmailp
fi
grep "^qmailq:" /etc/passwd >/dev/null || touch %{_tmppath}/qmailq-u
if [ -f %{_tmppath}/qmailq-u ]; then
    %{rootcmd} %{useradd} -d %{qdir} -g 400 -u 404 -M -r -s /bin/true qmailq
fi
grep "^qmailr:" /etc/passwd >/dev/null || touch %{_tmppath}/qmailr-u
if [ -f %{_tmppath}/qmailr-u ]; then
    %{rootcmd} %{useradd} -d %{qdir} -g 400 -u 405 -M -r -s /bin/true qmailr
fi
grep "^qmails:" /etc/passwd >/dev/null || touch %{_tmppath}/qmails-u
if [ -f %{_tmppath}/qmails-u ]; then
    %{rootcmd} %{useradd} -d %{qdir} -g 400 -u 406 -M -r -s /bin/true qmails
fi

make compile makelib
make it man
%if %{build_ldap}
make qldap
%endif


%install
export PATH="/sbin:/usr/sbin:/bin:/usr/bin"

### install directories ---------------------------------------------------
mkdir -p %{buildroot}%{_sysconfdir}/cron.hourly
mkdir -p %{buildroot}%{qdir}/{alias,control,owners,users,bin,man}
mkdir -p %{buildroot}{%{_libdir},%{_sbindir}}

# install
# we use custom qmail-install.sh script since we can't patch installer

cp %{SOURCE5} $RPM_BUILD_DIR/%{name}-%{version}
chmod u+x qmail-install.sh
export RPM_BUILD_ROOT=%{buildroot}
export RPM_BUILD_DIR=$RPM_BUILD_DIR
export NAME=%{name}
export VERSION=%{version}
export QDIR=%{qdir}
./qmail-install.sh

install -m 0755 instcheck %{buildroot}%{qdir}/bin
install -m 0755 config-fast %{buildroot}%{qdir}/bin

%if %{build_ldap}
for i in auth_imap auth_pop qmail-ldaplookup qmail-quotawarn qmail-reply
do
    install -m 0755 $i %{buildroot}%{qdir}/bin
done
%endif

%if %{build_msglog}
install -m 0644 %{SOURCE1} %{buildroot}%{qdir}/alias/.qmail-msglog
%endif

pushd %{buildroot}%{qdir}/alias
    echo "&nobody" > .qmail-postmaster
    ln -s .qmail-postmaster .qmail-mailer-daemon
popd

mkdir -p %{buildroot}%{_sysconfdir}/cron.hourly
install -m 0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/cron.hourly/qmail

install -m 0755 %{SOURCE3} %{buildroot}%{qdir}/rc
echo "./Maildir/" >%{buildroot}%{qdir}/control/defaultdelivery
mkdir -p %{buildroot}/var/log/qmail/{smtpd,pop3d,qmqpd,qmtpd}

mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
install -m 0755 %{SOURCE4} %{buildroot}%{_sysconfdir}/rc.d/init.d/qmail

pushd %{buildroot}%{qdir}/control
    touch defaultdomain me plusdomain rcpthosts
    # add localhost to locals file so programs like fetchmail can send mail to
    # user@localhost and it will be accepted
    echo "localhost" > locals
    # set remote and local concurrency limits; they can go no higher than that 
    # set in conf-spawn, which is 120 by default
    echo "90" > concurrencyremote
    echo "20" > concurrencylocal
    echo "20" > concurrencyincoming
    echo "20" > concurrencyqmqp
    echo "# you can add RBL sites to this file by using -r[host] (refer to rblsmtpd" > blacklists
    echo "#-rbl.spamcop.net" >> blacklists
    chmod 0644 *
popd

pushd %{buildroot}%{qdir}/users
    touch append assign cdb mailnames subusers
    chmod 0644 *
popd

# sendmail compatability links
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_libdir}
pushd %{buildroot}%{_sbindir}
    ln -s ../..%{qdir}/bin/sendmail sendmail
popd
pushd %{buildroot}%{_libdir}
    ln -s ../..%{qdir}/bin/sendmail sendmail
popd

cat <<EOFaliasempty >%{buildroot}%{qdir}/control/aliasempty
|dot-forward .forward
|preline procmail
EOFaliasempty

### Make for supervise
mkdir -p %{buildroot}%{qdir}/supervise/qmail-send/log
mkdir -p %{buildroot}%{qdir}/supervise/qmail-smtpd/log
mkdir -p %{buildroot}%{qdir}/supervise/qmail-pop3d/log
mkdir -p %{buildroot}%{qdir}/supervise/qmail-qmqpd/log
mkdir -p %{buildroot}%{qdir}/supervise/qmail-qmtpd/log

install -m 0755 %{SOURCE6} %{buildroot}%{qdir}/supervise/qmail-pop3d/run
install -m 0755 %{SOURCE7} %{buildroot}%{qdir}/supervise/qmail-pop3d/log/run
install -m 0755 %{SOURCE8} %{buildroot}%{qdir}/supervise/qmail-send/run
install -m 0755 %{SOURCE9} %{buildroot}%{qdir}/supervise/qmail-send/log/run
install -m 0755 %{SOURCE10} %{buildroot}%{qdir}/supervise/qmail-smtpd/run
install -m 0755 %{SOURCE11} %{buildroot}%{qdir}/supervise/qmail-smtpd/log/run
# qmqp
install -m 0755 %{SOURCE12} %{buildroot}%{qdir}/supervise/qmail-qmqpd/run
install -m 0755 %{SOURCE13} %{buildroot}%{qdir}/supervise/qmail-qmqpd/log/run
install -m 0755 %{SOURCE15} %{buildroot}%{qdir}/supervise/qmail-qmtpd/run
install -m 0755 %{SOURCE16} %{buildroot}%{qdir}/supervise/qmail-qmtpd/log/run

%if %{build_tls}
# TLS needs more memory in for qmail-smtpd
perl -pi -e 's|2000000|2500000|g;' %{buildroot}%{qdir}/supervise/qmail-smtpd/run
%endif

### Make /etc/tcprules.d/qmail-smtp
mkdir -p %{buildroot}%{_sysconfdir}/tcprules.d
# Setup default /etc/tcprules.d/qmail-smtp
cat <<EOFqmail-smtp >%{buildroot}%{_sysconfdir}/tcprules.d/qmail-smtp
127.:allow,RELAYCLIENT=""
EOFqmail-smtp

### Make /etc/tcprules.d/qmail-qmqp
# Setup default /etc/tcprules.d/qmail-qmqp
cat <<EOFqmail-qmqp >%{buildroot}%{_sysconfdir}/tcprules.d/qmail-qmqp
:deny
EOFqmail-qmqp

### Make /etc/tcprules.d/qmail-pop3
# Setup default /etc/tcprules.d/qmail-pop3
cat <<EOFqmail-pop3 >%{buildroot}%{_sysconfdir}/tcprules.d/qmail-pop3
127.:allow
EOFqmail-pop3

### Make /var/qmail/control/qmqpservers
cat <<EOF >%{buildroot}%{qdir}/control/qmqpservers
# List one IP address per line for QMQP servers that qmail-qmqpc will
# attempt to deliver to
EOF

mkdir -p %{buildroot}%{_sysconfdir}/skel/Maildir/{cur,new,tmp}
echo "./Maildir/" > %{buildroot}%{_sysconfdir}/skel/.qmail

find %{buildroot}%{qdir}/man -type f -exec bzip2 -9f {} \;

# additional TLS support
%if %{build_tls}
cat <<EOF >%{buildroot}%{qdir}/doc/make-cert
#!/bin/sh
/usr/bin/openssl req -new -x509 -nodes \
-out %{qdir}/control/servercert.pem -days 366 \
-keyout %{qdir}/control/servercert.pem
chmod 0640 %{qdir}/control/servercert.pem
chown qmaild.qmail %{qdir}/control/servercert.pem
ln -s %{qdir}/control/servercert.pem %{qdir}/control/clientcert.pem
EOF
cat <<EOF >%{buildroot}%{qdir}/doc/make-cert-req
#!/bin/sh
/usr/bin/openssl req -new -x509 -nodes \
-out %{qdir}/control/servercert.pem -days 366 \
-keyout %{qdir}/control/servercert.pem
/usr/bin/openssl req -new -nodes -out req.pem \
-keyout %{qdir}/control/servercert.pem
chmod 0640 %{qdir}/control/servercert.pem
chown qmaild.qmail %{qdir}/control/servercert.pem
ln -s %{qdir}/control/servercert.pem %{qdir}/control/clientcert.pem
echo ""
echo "Send req.pem to your CA to obtain signed_req.pem, and do:"
echo "cat signed_req.pem >> %{qdir}/control/servercert.pem"
EOF
chmod 0750 %{buildroot}%{qdir}/doc/make-cert
chmod 0750 %{buildroot}%{qdir}/doc/make-cert-req
%endif

%pre
### Before installation ---------------------------------------------------
# create groups and users
echo "Creating users and groups for qmail..."
grep "^qmail:" %{_sysconfdir}/group >/dev/null || groupadd -r -g 400 qmail
grep "^nofiles:" %{_sysconfdir}/group >/dev/null || groupadd -r -g 401 nofiles
grep "^alias:" %{_sysconfdir}/passwd >/dev/null || useradd -d %{qdir}/alias -g 401 -u 400 -M -r -s /bin/true alias
grep "^qmaild:" %{_sysconfdir}/passwd >/dev/null || useradd -d %{qdir} -g 401 -u 401 -M -r -s /bin/true qmaild
grep "^qmaill:" %{_sysconfdir}/passwd >/dev/null || useradd -d %{qdir} -g 401 -u 402 -M -r -s /bin/true qmaill
grep "^qmailp:" %{_sysconfdir}/passwd >/dev/null || useradd -d %{qdir} -g 401 -u 403 -M -r -s /bin/true qmailp
grep "^qmailq:" %{_sysconfdir}/passwd >/dev/null || useradd -d %{qdir} -g 400 -u 404 -M -r -s /bin/true qmailq
grep "^qmailr:" %{_sysconfdir}/passwd >/dev/null || useradd -d %{qdir} -g 400 -u 405 -M -r -s /bin/true qmailr
grep "^qmails:" %{_sysconfdir}/passwd >/dev/null || useradd -d %{qdir} -g 400 -u 406 -M -r -s /bin/true qmails

# Disable deliveries if upgrading
if [ $1 = 2 ]; then
    test -d %{qdir}/alias && chmod +t %{qdir}/alias
    test -d /home && chmod +t /home/*
fi

# Try to stop qmail daemons for those who do not stop it first
/sbin/service qmail stop >/dev/null 2>/dev/null || :


%preun
### Before un-installation ------------------------------------------------
# Try to stop qmail daemons for those who do not stop it first
# do a quick test to make sure qmail-send is running, if not don't execute
# the initscript or we get extra noise
TEST=`pidof qmail-send`
[[ -z $TEST ]] || /sbin/service qmail stop >/dev/null 2>/dev/null || :

chkconfig --del qmail


%post
### Post installation -----------------------------------------------------
# Re-enable deliveries if upgrading
if [ $1 = 2 ]; then
    test -d %{qdir}/alias && chmod -t %{qdir}/alias
    test -d /home && chmod -t /home/*
fi

# set up files in %{qdir}/control only if we are not upgrading 
if [ $1 = "1" ]; then
    (
    cd %{qdir}/bin
    ./config-fast $(hostname -f)
    # generate a proper queue/lock/tcpok file
    ./qmail-tcpok
    )
fi

if [ -f /usr/bin/tcprules ]; then
    echo "Compiling default cdb files in %{_sysconfdir}/tcprules.d..."
    /sbin/service qmail cdb
fi

echo "Please edit %{qdir}/alias/.qmail-postmaster and change the username of who to send postmaster/mailer-daemon messages to (currently is nobody)."

# manually run /etc/cron.hourly/qmail to initialize system:
echo "Initializing user base..."
sh %{_sysconfdir}/cron.hourly/qmail

if [ -f %{qdir}/doc/make-cert ]; then
    if [ ! -f %{qdir}/control/servercert.pem ]; then
        echo ""
        echo "Generating dummy self-signed certificate..."
        yes ""|sh %{qdir}/doc/make-cert >/dev/null 2>&1
        echo "You should create a proper certificate using either make-cert or"
        echo "make-cert-req in %{qdir}/doc to generate it."
    fi
fi

# add /var/qmail/man to manpath
if [ $1 = "1" ]; then
    echo "MANPATH /var/qmail/man" >>%{_sysconfdir}/man.config
fi

%_post_service qmail

%post qmqpd
if [ -f /usr/bin/tcprules ]; then
    echo "Compiling default cdb files in %{_sysconfdir}/tcprules.d..."
    /sbin/service qmail cdb
fi
if [ -f /var/lock/subsys/qmail ]; then
    /sbin/service qmail restart
fi


%postun
### Post uninstallation ----------------------------------------------------
# If qmail is removed (so not upgraded):
if [ $1 = 0 ]; then
    # this is needed for user* and group* programs
    export PATH=$PATH:/usr/sbin

    echo ""
    echo "Removing qmail users (if they exist):"

    for i in alias qmaild qmaill qmailp qmailq qmailr qmails; do
        %_postun_userdel $i
    done
    %_postun_groupdel qmail
    %_postun_groupdel nofiles

    ## update nis database
    if /sbin/pidof ypserv >/dev/null 2>/dev/null; then
        (cd /var/yp; make)
    fi

    # remove /var/qmail/man from manpath
    perl -pi -e 's|MANPATH /var/qmail/man||g' %{_sysconfdir}/man.config
fi


%preun qmqpd
# stop qmail before uninstalling qmqpd or supervise will have a cow
/sbin/service qmail stop >/dev/null 2>/dev/null || :

%postun qmqpd
/sbin/service qmail start >/dev/null 2>/dev/null || :


%preun pop3d
# stop qmail before uninstalling pop3d or supervise will have a cow
/sbin/service qmail stop >/dev/null 2>/dev/null || :

%postun pop3d
/sbin/service qmail start >/dev/null 2>/dev/null || :


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

# now we need to remove qmail users, but we check the semaphores we made
# in case this is being built on a system with qmail already installed
echo ""
echo "Removing qmail users if we added them:"

function user_del() {
    if [ -f %{_tmppath}/$1-u ]; then
        %{rootcmd} %{userdel} $1
        rm -f %{_tmppath}/$1-u
    fi
}
for i in alias qmaild qmaill qmailp qmailq qmailr qmails; do
    user_del $i
done

echo ""
echo "Removing qmail groups if we added them:"
function group_del() {
    if [ -f %{_tmppath}/$1-g ]; then
        %{rootcmd} %{groupdel} $1
        rm -f %{_tmppath}/$1-g
    fi
}

for i in nofiles qmail; do
    group_del $i
done

# cleanup any lingering tempfiles
rm -f %{_tmppath}/{{qmail,nofiles}-g,alias-u,qmail{d,l,p,q,r,s}-u}


%files
%defattr(-,-,qmail)
#docs
%attr(-,root,qmail) %doc BLURB BLURB2 BLURB3 BLURB4 CHANGES FAQ FILES README.RPM README.patches
%attr(-,root,qmail) %doc INSTALL INSTALL.* INTERNALS PIC.* README REMOVE.*
%attr(-,root,qmail) %doc SECURITY SENDMAIL TEST.* THANKS THOUGHTS TODO UPGRADE
%if %{build_smtpauth}
%attr(-,root,qmail) %doc README.auth
%endif
%if %{build_ldap}
%attr(-,root,qmail) %doc QLDAPTODO QLDAPPICTURE QLDAPNEWS QLDAPINSTALL
%endif

# config (system)
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/cron.hourly/qmail
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/rc.d/init.d/qmail
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/tcprules.d/qmail-smtp
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/skel/.qmail

# config (qmail)
%attr(0644,alias,nofiles) %config(missingok,noreplace) %{qdir}/alias/.qmail-*
%attr(0644,root,qmail) %config(missingok,noreplace) %{qdir}/control/defaultdomain
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/defaultdelivery
%attr(0644,root,qmail) %config(missingok,noreplace) %{qdir}/control/locals
%attr(0644,root,qmail) %config(missingok,noreplace) %{qdir}/control/plusdomain
%attr(0644,root,qmail) %config(missingok,noreplace) %{qdir}/control/rcpthosts
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/concurrencyincoming
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/concurrencylocal
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/concurrencyremote
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/aliasempty
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/me
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/blacklists
%attr(0644,root,qmail) %config(missingok,noreplace) %{qdir}/users/assign
%attr(0644,root,qmail) %config(missingok,noreplace) %{qdir}/users/cdb
%attr(0644,root,qmail) %config(noreplace) %{qdir}/users/append
%attr(0644,root,qmail) %config(noreplace) %{qdir}/users/mailnames
%attr(0644,root,qmail) %config(noreplace) %{qdir}/users/subusers
%attr(0755,root,qmail) %{qdir}/rc

# symlinks (sendmail)
%attr(-,root,qmail) %{_libdir}/sendmail
%attr(-,root,qmail) %{_sbindir}/sendmail

# directories
%attr(0755,root,qmail) %dir %{qdir}
%attr(2755,alias,qmail) %dir %{qdir}/alias
%attr(0755,root,qmail) %dir %{qdir}/bin
%attr(0755,root,qmail) %dir %{qdir}/boot
%attr(0755,root,qmail) %dir %{qdir}/control
%attr(0755,root,qmail) %dir %{qdir}/doc
%attr(0755,root,qmail) %dir %{qdir}/man
%attr(0755,root,qmail) %dir %{qdir}/man/man1
%attr(0755,root,qmail) %dir %{qdir}/man/man5
%attr(0755,root,qmail) %dir %{qdir}/man/man7
%attr(0755,root,qmail) %dir %{qdir}/man/man8
%attr(0750,qmailq,qmail) %dir %{qdir}/queue
%attr(0755,root,root) %dir %{qdir}/supervise
%attr(1755,root,root) %dir %{qdir}/supervise/qmail-send
%attr(1755,root,root) %dir %{qdir}/supervise/qmail-smtpd
%attr(0755,root,qmail) %dir %{qdir}/users
%attr(0755,qmaill,root) %dir /var/log/qmail
%attr(0755,qmaill,root) %dir /var/log/qmail/smtpd
%attr(0755,root,root) %dir %{_sysconfdir}/skel/Maildir
%attr(0755,root,root) %dir %{_sysconfdir}/skel/Maildir/cur
%attr(0755,root,root) %dir %{_sysconfdir}/skel/Maildir/new
%attr(0755,root,root) %dir %{_sysconfdir}/skel/Maildir/tmp

# qmail docs
%attr(0644,root,qmail) %{qdir}/doc/*

# supervise
%attr(0755,root,qmail) %{qdir}/supervise/qmail-send/run
%attr(0755,root,qmail) %{qdir}/supervise/qmail-send/log/run
%attr(0755,root,qmail) %{qdir}/supervise/qmail-smtpd/run
%attr(0755,root,qmail) %{qdir}/supervise/qmail-smtpd/log/run

# man pages
%attr(0644,root,qmail) %{qdir}/man/man1/qreceipt.1*
%attr(0644,root,qmail) %{qdir}/man/man1/condredirect.1*
%attr(0644,root,qmail) %{qdir}/man/man1/mailsubj.1*
%attr(0644,root,qmail) %{qdir}/man/man1/except.1*
%attr(0644,root,qmail) %{qdir}/man/man1/maildirmake.1*
%attr(0644,root,qmail) %{qdir}/man/man1/preline.1*
%attr(0644,root,qmail) %{qdir}/man/man1/tcp-env.1*
%attr(0644,root,qmail) %{qdir}/man/man1/bouncesaying.1*
%attr(0644,root,qmail) %{qdir}/man/man1/maildir2mbox.1*
%attr(0644,root,qmail) %{qdir}/man/man1/qbiff.1*
%attr(0644,root,qmail) %{qdir}/man/man1/forward.1*
%attr(0644,root,qmail) %{qdir}/man/man1/maildirwatch.1*
%attr(0644,root,qmail) %{qdir}/man/man5/qmail-users.5*
%attr(0644,root,qmail) %{qdir}/man/man5/maildir.5*
%attr(0644,root,qmail) %{qdir}/man/man5/qmail-header.5*
%attr(0644,root,qmail) %{qdir}/man/man5/envelopes.5*
%attr(0644,root,qmail) %{qdir}/man/man5/mbox.5*
%attr(0644,root,qmail) %{qdir}/man/man5/tcp-environ.5*
%attr(0644,root,qmail) %{qdir}/man/man5/qmail-control.5*
%attr(0644,root,qmail) %{qdir}/man/man5/qmail-log.5*
%attr(0644,root,qmail) %{qdir}/man/man5/addresses.5*
%attr(0644,root,qmail) %{qdir}/man/man5/dot-qmail.5*
%attr(0644,root,qmail) %{qdir}/man/man7/qmail-limits.7*
%attr(0644,root,qmail) %{qdir}/man/man7/forgeries.7*
%attr(0644,root,qmail) %{qdir}/man/man7/qmail.7*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-tcpto.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-qread.8*
%attr(0644,root,qmail) %{qdir}/man/man8/splogger.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-start.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-newu.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-tcpok.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-inject.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-clean.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-getpw.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-command.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-showctl.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-rspawn.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-smtpd.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-qstat.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-pw2u.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-queue.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-popup.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-lspawn.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-newmrh.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-local.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-send.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-remote.8*

# qmail queue
%attr(0700,qmails,qmail) %dir %{qdir}/queue/bounce
%attr(0700,qmails,qmail) %dir %{qdir}/queue/info
%attr(0700,qmails,qmail) %{qdir}/queue/info/*
%attr(0700,qmailq,qmail) %dir %{qdir}/queue/intd
%attr(0700,qmails,qmail) %dir %{qdir}/queue/local
%attr(0700,qmails,qmail) %{qdir}/queue/local/*
%attr(0750,qmailq,qmail) %dir %{qdir}/queue/lock
%attr(0600,qmails,qmail) %{qdir}/queue/lock/sendmutex
%attr(0644,qmailr,qmail) %{qdir}/queue/lock/tcpto
# mkfifo -m 0622 trigger
%attr(-,qmails,qmail) %{qdir}/queue/lock/trigger
%attr(0750,qmailq,qmail) %dir %{qdir}/queue/mess
%attr(0750,qmailq,qmail) %{qdir}/queue/mess/*
%attr(0700,qmailq,qmail) %dir %{qdir}/queue/pid
%attr(0700,qmails,qmail) %dir %{qdir}/queue/remote
%attr(0700,qmails,qmail) %{qdir}/queue/remote/*
%attr(0750,qmailq,qmail) %dir %{qdir}/queue/todo

# boot files
%attr(0755,root,qmail) %{qdir}/boot/home
%attr(0755,root,qmail) %{qdir}/boot/home+df
%attr(0755,root,qmail) %{qdir}/boot/binm1
%attr(0755,root,qmail) %{qdir}/boot/binm2+df
%attr(0755,root,qmail) %{qdir}/boot/proc+df
%attr(0755,root,qmail) %{qdir}/boot/binm2
%attr(0755,root,qmail) %{qdir}/boot/binm3
%attr(0755,root,qmail) %{qdir}/boot/proc
%attr(0755,root,qmail) %{qdir}/boot/binm3+df
%attr(0755,root,qmail) %{qdir}/boot/binm1+df

# binaries
%attr(0755,root,qmail) %{qdir}/bin/bouncesaying
%attr(0755,root,qmail) %{qdir}/bin/condredirect
%attr(0755,root,qmail) %{qdir}/bin/config-fast
%attr(0755,root,qmail) %{qdir}/bin/datemail
%attr(0755,root,qmail) %{qdir}/bin/elq
%attr(0755,root,qmail) %{qdir}/bin/except
%attr(0755,root,qmail) %{qdir}/bin/forward
%attr(0755,root,qmail) %{qdir}/bin/instcheck
%attr(0755,root,qmail) %{qdir}/bin/maildir2mbox
%attr(0755,root,qmail) %{qdir}/bin/maildirmake
%attr(0755,root,qmail) %{qdir}/bin/maildirwatch
%attr(0755,root,qmail) %{qdir}/bin/mailsubj
%attr(0755,root,qmail) %{qdir}/bin/pinq
%attr(0755,root,qmail) %{qdir}/bin/predate
%attr(0755,root,qmail) %{qdir}/bin/preline
%attr(0755,root,qmail) %{qdir}/bin/qail
%attr(0755,root,qmail) %{qdir}/bin/qbiff
%attr(0711,root,qmail) %{qdir}/bin/qmail-clean
%attr(0711,root,qmail) %{qdir}/bin/qmail-getpw
%attr(0755,root,qmail) %{qdir}/bin/qmail-inject
%attr(0711,root,qmail) %{qdir}/bin/qmail-local
%attr(0700,root,qmail) %{qdir}/bin/qmail-lspawn
%attr(0700,root,qmail) %{qdir}/bin/qmail-newmrh
%attr(0700,root,qmail) %{qdir}/bin/qmail-newu
%attr(0711,root,qmail) %{qdir}/bin/qmail-pw2u
%attr(0755,root,qmail) %{qdir}/bin/qmail-qread
%attr(0755,root,qmail) %{qdir}/bin/qmail-qstat
%attr(04711,qmailq,qmail) %{qdir}/bin/qmail-queue
%attr(0711,root,qmail) %{qdir}/bin/qmail-remote
%attr(0711,root,qmail) %{qdir}/bin/qmail-rspawn
%attr(0711,root,qmail) %{qdir}/bin/qmail-send
%attr(0755,root,qmail) %{qdir}/bin/qmail-showctl
%attr(0755,root,qmail) %{qdir}/bin/qmail-smtpd
%attr(0700,root,qmail) %{qdir}/bin/qmail-start
%attr(0755,root,qmail) %{qdir}/bin/qmail-tcpok
%attr(0755,root,qmail) %{qdir}/bin/qmail-tcpto
%attr(0755,root,qmail) %{qdir}/bin/qreceipt
%attr(0755,root,qmail) %{qdir}/bin/qsmhook
%attr(0755,root,qmail) %{qdir}/bin/sendmail
%attr(0711,root,qmail) %{qdir}/bin/splogger
%attr(0755,root,qmail) %{qdir}/bin/tcp-env
%if %{build_ldap}
%attr(0755,root,qmail) %{qdir}/bin/auth_imap
%attr(0755,root,qmail) %{qdir}/bin/auth_pop
%attr(0755,root,qmail) %{qdir}/bin/qmail-ldaplookup
%attr(0755,root,qmail) %{qdir}/bin/qmail-quotawarn
%attr(0755,root,qmail) %{qdir}/bin/qmail-reply
%endif
%if %{build_tls}
%attr(0755,root,qmail) %{qdir}/bin/mkqmailcert
%endif


%files pop3d
%defattr(-,-,qmail)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/tcprules.d/qmail-pop3
%attr(1755,root,root) %dir %{qdir}/supervise/qmail-pop3d
%attr(0755,root,qmail) %{qdir}/supervise/qmail-pop3d/run
%attr(0755,root,qmail) %{qdir}/supervise/qmail-pop3d/log/run
%attr(0755,qmaill,root) %dir /var/log/qmail/pop3d
%attr(0755,root,qmail) %{qdir}/bin/qmail-pop3d
%attr(0711,root,qmail) %{qdir}/bin/qmail-popup
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-pop3d.8*


%files qmqpd
%defattr(-,-,qmail)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/tcprules.d/qmail-qmqp
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/concurrencyqmqp
%attr(1755,root,root) %dir %{qdir}/supervise/qmail-qmqpd
%attr(0755,root,qmail) %{qdir}/supervise/qmail-qmqpd/run
%attr(0755,root,qmail) %{qdir}/supervise/qmail-qmqpd/log/run
%attr(0755,qmaill,root) %dir /var/log/qmail/qmqpd
%attr(1755,root,root) %dir %{qdir}/supervise/qmail-qmtpd
%attr(0755,root,qmail) %{qdir}/supervise/qmail-qmtpd/run
%attr(0755,root,qmail) %{qdir}/supervise/qmail-qmtpd/log/run
%attr(0755,qmaill,root) %dir /var/log/qmail/qmtpd
%attr(0644,root,qmail) %config(missingok,noreplace) %{qdir}/control/qmqpservers
%attr(0755,root,qmail) %{qdir}/bin/qmail-qmqpc
%attr(0755,root,qmail) %{qdir}/bin/qmail-qmqpd
%attr(0755,root,qmail) %{qdir}/bin/qmail-qmtpd
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-qmqpd.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-qmtpd.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-qmqpc.8*


%changelog
* Tue Aug 23 2005 Vincent Danen <vdanen@mandrakesoft.com> 1.03-26avx
- convert it into a ports package for Annvix
- NOTE: there are a lot of things to do with this spec still, but I don't
  have the time to at the moment:
  - it needs to be able to build without root and without the qmail users
    pre-existing (ie. patch out whatever we have to do to do this)
  - remove the initscript
  - change the deps from daemontools to ipsvd and change runscripts
  - relocate runscripts?  maybe put the whole thing in /usr/local/var/qmail?
  - probably a whole lot of cleaning (what a mess!)
  - maybe use netqmail 1.05 instead?
  - we can patch the crap out of this sucker now and still comply with djb's
    silly license since it will never be distributed in binary form (yippee!)

* Fri Sep 19 2003 Vincent Danen <vdanen@mandrakesoft.com> 1.03-25rph
- support for 9.2
- use a sub-release now to indicate what platform we're built for
- remove support for 7.x and 8.x (sorry folks); this makes it easier to
  maintain

* Thu Aug 14 2003 Vincent Danen <vdanen@mandrakesoft.com> 1.03-24rph
- defaultdelivery now contains ./Maildir/ (re: Shekhar Joshi)
- run qmail-tcpok when executing doqueue (re: Shekhar Joshi)
- don't enable any RBL by default (re: Mark Watts)

* Mon Mar 17 2003 Vincent Danen <vdanen@mandrakesoft.com> 1.03-23rph
- liberal application of %%{build_91} macros where required
- three new macros:  %%{rootcmd}, %%{useradd}, and %%{groupadd}; only used
  during the building phase.  This will allow you to use sudo or an equivalent
  program to call useradd/groupadd as root during the build and cleanup
  phases only (this is suitable if you want to build as non-root but have root
  privs on your system and can give yourself sudo access)

* Sun Mar  9 2003 Paul Cox <paul@coxcentral.com> 1.03-22rph
- Patch101: fix errno build error for 9.1
- edited Source5 (qmail-install.sh) to comment out cat1, cat5, cat7, and
  cat8 stuff; was not listed in files list so rpm was barfing at the end
  of building when checking for installed but not used files

* Thu Dec  4 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.03-21rph
- remove build_xx macros; ripped some auto-detection from the samba specs so
  if you build on a 9.0 system, it will build for 9.0 automatically, etc.
- make P100 an optional patch as well (--build msglog); no more
  .qmail-msglog unless you ask for it
- automatic generation of tls certs wasn't working in %%post for some
  reason; fixed
- throw a %%_post_service qmail in %%post because otherwise we have to
  manually restart qmail after upgrade
- change softlimit to 3200000 all across the board, should yield better
  performance
- add rblsmtpd support to qmail-smtpd by default; see
  %{qdir}/control/blacklists and %{qdir}/supervise/qmail-smtpd/run; defaults
  to bl.spamcop.net (anti-UCE support)
- add -R to all tcpserver calls (do not attempt to obtain $TCPREMOTEINFO),
  which will help speed up services coming from hosts without identd info
  available (misconfigured firewalls, etc.)
- this spec is becoming entirely too unmanageable =)

* Thu Aug 15 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.03-20rph
- P100 modifies extra.h to allow logging every message via
  ~alias/.qmail-msglog.  Thanks to Adrian Stanciu for pointing out that the
  .qmail-msglog file does nothing without enabling QUEUE_EXTRA.
- add the concurrencyincoming control file (only used in smtpd/run) to
  control the number of incoming SMTP connections; default is 20
- make starting and stopping qmail during upgrades quieter and hopefully
  less finicky with service starting zombies
- make pop3d %%preun and %%postun stop/start qmail just like qmqpd so
  service doesn't freak out
- rewrite parts of the initscript to make it more uniform with the other
  system initscripts
- add the concurrencyqmqp file (only used in qmqpd/run) to control the
  number of incoming QMQP connections; default is 20
- you should now be able to build the rpm as non-root provided the qmail
  users already exist on the system (implies 8.1/8.2 or qmail already
  installed)  FINALLY!
- add /var/qmail/man to MANPATH on install; remove it on uninstall
- remove /var/qmail/man/cat* from packages

* Fri Aug  9 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.03-19rph
- build_90 macro for building for cooker/9.0+; unfortunately we can't use
  the %%_pre_useradd macro yet because we need to specify a group and the
  macro can't handle it, so we do things exactly the same as we did for 7.2
- build_8x macro for building 8.1/8.2 since the default is now to build for
  9.0
- new TLS patch (20020801)

* Tue Jun 11 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.03-18rph
- Changes from Alexander Skwar <ASkwar@DigitalProjects.com>:
  - Add yet another build option: nocrammd5.  If also smtpauth is specified,
    it will build qmail without CRAM-MD5 support.  Furthermore, cmd5checkpw
    will not be Require:'d
  - NOTE: Currently you cannot build qmail with TLS and smtp-auth.  You also
    cannot build with both TLS and LDAP.
- YABO: --with dietlibc; this will build qmail against dietlibc
- updated qmail package description
- only unarchive the smtp-auth source if we are building --with smtpauth
- smtp-auth patch v0.31
- use newer tls patch (20020526)
- force the spec to undefine TLS support if either LDAP or smtp-auth are
  defined (since you can't build those combinations anyway) 
- make changes to /etc/cron.hourly/qmail to make it more vpopmail friendly;
  it will no longer overwrite the assign file but will append new entries to
  it that are found on the system (thanks to Sebastien <sebest@3ie.org>)
- finally fix nested %%if's

* Mon Apr 15 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.03-17rph
- create a qmail-pop3d subpackage to provide POP3 support
- move QMQP/QMTP-related binaries and manpages into qmail-qmqpd package
- use $PASSPROG in /var/qmail/supervise/qmail-pop3d/run to better accomodate
  checkpassword or checkvpw (for use with vmailmgr)
- modify /etc/cron.hourly/qmail to work a little nicer with NIS/LDAP based
  systems (use getent passwd instead of reading /etc/passwd directly as some
  users may be missing this way)... this lets us have the ability to use
  qmail on systems using LDAP authentication for the base system (should
  work with NIS also)
- have initscript silently try to kill all qmail services before starting
  just in case (re: tlyons@mandrakesoft.com)
- use new rph extension

* Tue Dec 11 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.03-16mdk
- fix bad placement for concurrency limits... conf-spawn defaults to 120, it
  is /var/qmail/control/concurrency{local,remote} that controls the number
  of simultaneous deliveries; set this to 90 for remote and 20 for local
  (defaults are 20 and 10 respectively)
- new option: --with ldap; builds qmail ldap support (thanks Todd)
- modify supervise/qmail-smtpd/run so that you can easily change $SMTPD to
  use a replacement for qmail-smtpd (ie. reisersmtpd, which uses lmail-smtpd)
- NOTE: you cannot use the LDAP patch with the TLS patch and, it looks like,
  the smtpd-auth patch.  If you want LDAP support, you can't have the
  security features like TLS and smtp-auth (right now, anyways)
- initscript sources functions (re: Yura Gusev)

* Tue Dec 11 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.03-15mdk
- include /var/qmail/supervise/qmail-qmtpd for QMTP daemon in qmqpd package
- update initscript for QMTP support
- install empty /var/qmail/control/qmqpservers config file
- make the concurrency limit a little higher since this must be used on
  pentium+ systems (now 90 instead of 20).
- include qmail-smtpd-auth 0.30 patch

* Fri Nov 30 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.03-14mdk
- by default we build for 8.1; no need to use "--with 8.1"
- add RPMOPTIONS to README.RPM (to see what --with definitions are used in
  the build)
- new option: --with qmailqueue; this will apply the qmailqueue patch from
  Bruce Guenter
- new file, README.patches with info on the patches that can be applied
  during a rebuild
- new option: --with tls; this will apply the qmail TLS patch from Frederik
  Vermeulen
- new option: --with linksync; this is to sync metadata for ReiserFS from
  Frank Denis
- (this spec is getting *really* ugly now... aaargh)

* Thu Sep 27 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.03-13mdk
- new package with support for 8.1 (--with-8.1) that does not add any users
  at build or install

* Fri Sep  7 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.03-12mdk
- macros to determine what we build for: --with-8.0 for 8.0+ or
  --with-7.2 for 7.2; we do this because 8.0+ have qmail users defined
  by default

* Sat Apr 14 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.03-11mdk
- added README.RPM which describes build environment

* Sun Feb 25 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.03-10mdk
- added qmail-qmqp sub-package which provides support for qmqp
- rewrote initscript to compile tcp rules for qmqp and pop3 if they exist
- added conditional statements to initscript so it does not croak if pop3
  support is removed

* Sat Dec 30 2000 Vincent Danen <vdanen@mandrakesoft.com> 1.03-9mdk
- install now builds tcprules files; previous version didn't which prevented
  qmail from starting automatically
- include /var/qmail/supervise/pop3d in directory list with proper
  permissions so supervise can run the logger as well

* Sat Oct 28 2000 Vincent Danen <vdanen@mandrakesoft.com> 1.03-8mdk
- more macros
- no longer create a qmail-source package
- call qmail-pop3d from supervise, not inetd
- created supervise scripts (source files), removed the auto-generation 
  from the spec file (this is cleaner)
- fix bad routine for creating users during build (clean would remove the
  users whether we added them during build or not)
- removed /usr/man/{man1,man5,man7,man8} from the file list (we don't own
  them)
- removed symlinks for manpages.  a better solution would be to add another
  MANPATH statement to /etc/man.config to point to /var/qmail/man

* Sun Aug  6 2000 Vincent Danen <vdanen@mandrakesoft.com> 1.03-7mdk
- echo localhost to control/locals so qmail delivers mail locally by
  default
- include qmail-install.sh, a custom qmail installer for building this
  RPM (since we can't patch the installer)
- use semaphores in _tmppath to determine if we added qmail users/groups
  during install, and if we did, remove them on clean
- add call to bin/qmail-tcpok to generate a proper queue/lock/tcpok file
- call /etc/cron.hourly/qmail in post to initialize userbase
- fix bad manpage symlinks

* Wed Aug  2 2000 Vincent Danen <vdanen@mandrakesoft.com> 1.03-6mdk
- remove /var/qmail/users{include,exclude} as they interfere with
  proper delivery
- fix cron.hourly/qmail
- fix sendmail symlinks

* Sun Jul 30 2000 Vincent Danen <vdanen@mandrakesoft.com> 1.03-5mdk
- force attr on every single file, for owner/group and perms
- more macros

* Wed Jul 19 2000 Vincent Danen <vdanen@mandrakesoft.com> 1.03-4mdk
- added entries in /etc/skel for maildir support
- manual bzip manpages since they are in non-standard location

* Tue Jul 18 2000 Vincent Danen <vdanen@mandrakesoft.com> 1.03-3mdk
- fix more permissions so logging will work properly

* Mon Jul 17 2000 Vincent Danen <vdanen@mandrakesoft.com> 1.03-2mdk
- fix /etc/cron.hourly/qmail
- /etc/tcprules.d/ was excluded, now it's included properly
- fix symlinks for sendmail
- left out defaultdelivery by accident
- fix bad homedir for user alias (was /etc/qmail/alias, should be
  /var/qmail/alias)
- fix /etc/rc.d/init.d/qmail so chkconfig recognizes it properly

* Mon Jul 17 2000 Vincent Danen <vdanen@mandrakesoft.com> 1.03-1mdk
- first mandrake spec, based on specs from Geoffrey Lee
  <snailtalk@linux-mandrake.com> and Bruce Guenter <bruceg@em.ca>
- many enhancements, follows Life with Qmail install process
