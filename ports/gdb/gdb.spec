#
# spec file for ports package gdb
#
# Ports Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments to the maintainer of this package:
#
#   ying@annvix.org
#
# $Id$
#
# RH 6.3.0.0-1.49

%define name		gdb
%define version		6.3
%define release		2avx

%define _prefix		/usr/local
%define _mandir		/usr/local/share/man
%define _infodir	/usr/local/share/info
%define _sysconfdir	/usr/local/etc
%define _docdir		/usr/local/share/doc


Summary:	A GNU source-level debugger for C, C++ and Fortran
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
URL:		http://www.gnu.org/software/gdb/
Group:		Development/Other
Source0:	http://ftp.gnu.org/gnu/gdb/gdb-%{version}.tar.bz2
# Fix sim build
Patch1:		gdb-5.2.1-fix-sim-build.patch
Patch2:		gdb-6.3-system-readline.patch
Patch3:		gdb-6.0-tracepoint.patch
##
# Red Hat patches
##
Patch10:	gdb-6.3-rh-changelogs-20041202.patch
# Work around out-of-date dejagnu that does not have KFAIL
Patch11:	gdb-6.3-rh-dummykfail-20041202.patch
# Match Red Hat's version info
Patch12:	gdb-6.3-rh-testversion-20041202.patch
# Check that libunwind works - new test then fix
Patch13:	gdb-6.3-rh-testlibunwind-20041202.patch
Patch14:	gdb-6.3-rh-testlibunwind1fix-20041202.patch
# Recognize i386 signal trampolines before CFI.  Ensures that signal
# frames are identified as signal frames.
Patch101:	gdb-6.3-sigx86-20040621.patch
# Don't reject signal trampoline frames that have a [data] symbol
# associated with them as occures when backtracing through an
# alt-stack in the data address space.
Patch102:	gdb-6.3-sigsymtramp-20040621.patch
# Add unwinders for PPC and PPC64 signal trampolines.
Patch103:	gdb-6.3-ppcsignals-20040621.patch
# Use convert_from_func_ptr_addr on the solib breakpoint address;
# simplifies and makes more consistent the logic.
Patch104:	gdb-6.3-ppcdotsolib-20041022.patch
# Better parse 64-bit PPC system call prologues.
Patch105:	gdb-6.3-ppc64syscall-20040622.patch
# Stop a backtrace when a zero PC is encountered.
Patch106:	gdb-6.3-framepczero-20040927.patch
# Hack around broken header files that incorrectly define the FPSCR
# macro.
Patch107:	gdb-6.3-ppc64fpscrhack-20041026.patch
# Pass the pc's section into the symbol search code; stops the lookup
# finding a symbol from the wrong section.
Patch108:	gdb-6.3-ppc64section-20041026.patch
# Add PPC register groups so that info registers et.al.; along with
# register save and restore; work better.  On PPC-64 it was restoring
# the PS register setting the break-on-branch bit!
Patch109:	gdb-6.3-ppcreggroups-20041124.patch
# Fix up 64-bit PPC inferior function calls so that function
# parameters are passed correctly.
Patch110:	gdb-6.3-ppc64abi-20040621.patch
# Include the pc's section when doing a symbol lookup so that the
# correct symbol is found.
Patch111:	gdb-6.3-ppc64displaysymbol-20041124.patch
# Fix stepping in threads
Patch112:	gdb-6.3-thread-step-20041207.patch
# Threaded watchpoint support
Patch113:	gdb-6.3-threaded-watchpoints-20041213.patch
# Multiple patches to ia64 backtrace
Patch114:	gdb-6.3-ia64-backtrace-20041213.patch
# Fix to expose multiple constructors to end-user
Patch115:	gdb-6.3-constructor-20041216.patch
# Fix to display base constructors from list and breakpoint commands
Patch116:	gdb-6.3-linespec-20041213.patch
# Continue removing breakpoints even when failure occurs.
Patch117:	gdb-6.3-removebp-20041130.patch
# Add a wrapper script to GDB that implements pstack using the
# --readnever option.
Patch118:	gdb-6.3-gstack-20050411.patch
# Fix for caching thread lwps for linux
Patch119:	gdb-6.3-lwp-cache-20041216.patch
# Fix to ensure types are visible
Patch120:	gdb-6.3-type-fix-20041213.patch
# Fix for allowing macros to continue after backtrace errors
Patch121:	gdb-6.3-backtrace-20041216.patch
# VSYSCALL and PIE
Patch122:	gdb-6.3-test-pie-20050107.patch
Patch123:	gdb-6.3-vsyscall-20041216.patch
Patch124:	gdb-6.3-pie-20050110.patch
# Get selftest working with sep-debug-info
Patch125:	gdb-6.3-test-self-20050110.patch
# No longer a need to set .malloc on ppc64.
Patch126:	gdb-6.3-ppcmalloc-20041124.patch
# Enable PPC CFI support.
Patch127:	gdb-6.3-ppccfi-20041104.patch
# Fix for non-threaded watchpoints.
Patch128:	gdb-6.3-nonthreaded-wp-20050117.patch
# Add synthetic symbols (esp PPC-64 .symbols) to min symtab
Patch129:	gdb-6.3-ppcdotsym-20050126.patch
# Add PPC .symbols to min-symtable.
Patch130:	gdb-6.3-ctorline-20050120.patch
# Handle nested, and back-to-back signals when stepping.
Patch131:	gdb-6.3-sigrepeats-20050121.patch
Patch132:	gdb-6.3-test-sigrepeats-20050121.patch
# Fix to support multiple destructors just like multiple constructors
Patch133:	gdb-6.3-test-dtorfix-20050121.patch
Patch134:	gdb-6.3-dtorfix-20050121.patch
# Fix for ia64 to prevent SIGSEGV in debugger
Patch135:	gdb-6.3-ia64fix-20050121.patch
# Fix to support executable moving
Patch136:	gdb-6.3-test-movedir-20050125.patch
Patch137:	gdb-6.3-movedir-20050125.patch
# Fix to support unwinding syscalls in ia64 corefiles
Patch138:	gdb-6.3-ia64-corefile-fix-20050127.patch
# Tolerate DW_AT_type referencing <0>.
Patch139:	gdb-6.3-dwattype0-20050201.patch
# Fix gcore for threads
Patch140:	gdb-6.3-gcore-thread-20050204.patch
# Fix stepping over thread exit
Patch141:	gdb-6.3-step-thread-exit-20050211.patch
# Prevent gdb from being pushed into background
Patch142:	gdb-6.3-terminal-fix-20050214.patch
# Fix for unload.exp testcase
Patch143:	gdb-6.3-unload-test-20050216.patch
# Backport addition symfile-mem.o to all GNU/Linux systems.
Patch144:	gdb-6.3-addsymfilemem-20050209.patch
# Allow sibling threads to set threaded watchpoints for x86 and x86-64
Patch145:	gdb-6.3-threaded-watchpoints2-20050225.patch
# Follow vfork fix from mainline sources
Patch146:	gdb-6.3-follow-vfork-20050303.patch
# Fix unexpected compiler warning messages.
Patch147:	gdb-6.3-warnings-20050317.patch
# Fix printing of inherited members
Patch148:	gdb-6.3-inheritance-20050324.patch
# Add vsyscall page support for ia64.
Patch149:	gdb-6.3-ia64-vsyscall-20050330.patch
# Print a warning when the separate debug info's CRC doesn't match.
Patch150:	gdb-6.3-test-sepcrc-20050402.patch
Patch151:	gdb-6.3-sepcrc-20050402.patch
# Handle read side of DW_OP_piece.
Patch152:	gdb-6.3-dwoppieceread-20050407.patch
# Do not issue warning message about first page of storage for ia64 gcore
Patch153:	gdb-6.3-ia64-gcore-page0-20050421.patch
# Ia64 patch for added libunwind support
Patch154:	gdb-6.3-ia64-sigtramp-20050427.patch
# Partial die in cache fix
Patch155:	gdb-6.3-partial-die-20050503.patch
# SA_RESTART patch
Patch156:	gdb-6.3-sarestart-20050518.patch
# Security errata for bfd overflow and untrusted .gdbinit
Patch157:	gdb-6.3-security-errata-20050610.patch
# IA64 sigtramp prev register patch
Patch158:	gdb-6.3-ia64-sigtramp-frame-20050708.patch
# IA64 sigaltstack patch
Patch159:	gdb-6.3-ia64-sigaltstack-20050711.patch
# IA64 gcore speed-up patch
Patch160:	gdb-6.3-ia64-gcore-speedup-20050714.patch
# Notify observers that the inferior has been created
Patch161:	gdb-6.3-inferior-notification-20050721.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	ncurses-devel readline-devel texinfo flex bison

PreReq:		info-install

%description
Gdb is a full featured, command driven debugger. Gdb allows you to
trace the execution of programs and examine their internal state at
any time.  Gdb works for C and C++ compiled with the GNU C compiler
gcc.


%prep
%setup -q
%patch1 -p1 -b .sim-fixes
%patch2 -p1 -b .system-readline
%patch3 -p1 -b .tracepoint
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch110 -p1
%patch111 -p1
%patch112 -p1
%patch113 -p1
%patch114 -p1
%patch115 -p1
%patch116 -p1
%patch117 -p1
%patch118 -p1
%patch119 -p1
%patch120 -p1
%patch121 -p1
%patch122 -p1
%patch123 -p1
%patch124 -p1
%patch125 -p1
%patch126 -p1
%patch127 -p1
%patch128 -p1
%patch129 -p1
%patch130 -p1
%patch131 -p1
%patch132 -p1
%patch133 -p1
%patch134 -p1
%patch135 -p1
%patch136 -p1
%patch137 -p1
%patch138 -p1
%patch139 -p1
%patch140 -p1
%patch141 -p1
%patch142 -p1
%patch143 -p1
%patch144 -p1
%patch145 -p1
%patch146 -p1
%patch147 -p1
%patch148 -p1
%patch149 -p1
%patch150 -p1
%patch151 -p1
%patch152 -p1
%patch153 -p1
%patch154 -p1
%patch155 -p1
%patch156 -p1
%patch157 -p1
%patch158 -p1
%patch159 -p1
%patch160 -p1
%patch161 -p1
rm -rf ./gdb/gdbserver

cat > gdb/version.in << EOF
%{version}-%{release}
EOF


%build
%define __libtoolize :
%configure \
    --with-separate-debug-dir=%{_prefix}/lib/debug
%make
make info


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

# The above is broken, do this for now:
mkdir -p %{buildroot}%{_infodir}
cp `find . -name "*.info*"` %{buildroot}%{_infodir}
rm -f %{buildroot}%{_infodir}/dir %{buildroot}%{_infodir}/dir.info* 
rm -f %{buildroot}%{_bindir}/{texindex,texi2dvi,makeinfo,install-info,info}

# These are part of binutils
rm -f %{buildroot}%{_infodir}/{bfd,standard,readline,history,info,texinfo}*
rm -fr %{buildroot}%{_includedir}
rm -fr %{buildroot}%{_libdir}/lib{bfd*,opcodes*,iberty*}

# Remove even more unpackaged files
rm -f %{buildroot}%{_libdir}/libmmalloc.a
rm -f %{buildroot}%{_infodir}/{configure,libiberty,rluserman}.info*
rm -rf %{buildroot}%{_datadir}/locale/
rm -f %{buildroot}%{_infodir}/annotate.info*


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info gdb.info
%_install_info gdbint.info
%_install_info stabs.info


%preun
if [ $1 = 0 ]; then
    %_remove_install_info gdb.info
    %_remove_install_info gdbint.info
    %_remove_install_info stabs.info
fi


%files
%defattr(-,root,root)
%doc COPYING COPYING.LIB README gdb/NEWS
%{_bindir}/gdb
%{_bindir}/gdbtui
%{_bindir}/gstack
%ifarch ppc
%{_bindir}/run
%{_mandir}/man1/run.1*
%endif
%{_mandir}/man1/gdb.1*
%{_mandir}/man1/gdbtui.1*
%{_infodir}/gdb.info*
%{_infodir}/gdbint.info*
%{_infodir}/stabs.info*


%changelog
* Thu Aug 26 2005 Ying-Hung Chen <ying@annvix.org> 6.3-2avx
- Fix Source0 link
- Added archive.md5sum

* Mon Aug 15 2005 Vincent Danen <vdanen@annvix.org> 6.3-1avx
- first Annvix ports package; originally submitted by ying@annvix.org but I
  discarded it to use Mandriva's package as a base as it had less cleaning
  to do

* Sun Jul 31 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 6.3-5mdk
- add BuildRequires: bison

* Tue Jul 26 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 6.3-4mdk
- merge with RH 6.3.0.0-1.49

* Thu Jan 20 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 6.3-3mdk
- rebuild for new readline
- wipe out buildroot at the beginning of %%install

* Sun Nov 14 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 6.3-2mdk
- add BuildRequires: flex

* Wed Nov 10 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 6.3-1mdk
- 6.3

* Thu Aug 26 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 6.2-2mdk
- Improved i386 prologue analyzer from 6.2-branch (2004/07/08)

* Wed Aug 25 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 6.2-1mdk
- 6.2

* Fri Aug 13 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 6.1.1-2mdk
- Rebuild for new conversion table menu

* Fri Jul 30 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 6.1.1-1mdk
- package ppc-specific files
- 6.1.1

* Mon May 24 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 6.1-1mdk
- 6.1

* Thu Jan 15 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 6.0-2mdk
- Updates from 6.0-branch to fix other dwarf2 related bugs

* Thu Jan  7 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 6.0-1mdk
- 6.0

* Tue Sep  9 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.3-26mdk
- debuginfo dir is always %%{_prefix}/lib/debug

* Mon Jun 17 2003 Stefan van der Eijk <stefan@eijk.nu> 5.3-25mdk
- BuildRequires

* Tue Apr 15 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.3-24mdk
- Fix build on x86-64

* Wed Apr  2 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.3-23mdk
- Should be -3mdk but the icons fix required 20 releases ;-)
- Patch2: Cleanup cfi engine on rerun (Michal Ludvig)
- Patch3: Added ability to do backtrace from some functions without
  debug info on dwarf2 targets, e.g. x86-64 (Michal Ludvig)
- Patch4: Accept empty args through --args (Andreas Schwab)
- Patch5: Add support for external debug symbols (Jim Blandy, Alex Larsson)
- Patch6: Ignore NOBITS .eh_frame section in debug info (Elena Zannoni)
- Patch7: Handle files with stabs debug info but no line info (Jeff
  Johnston, RH #84253)

* Thu Feb 27 2003 David BAUDENS <baudens@mandrakesoft.com> 5.3-22mdk
- Fix icons

* Tue Dec 24 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.3-1mdk
- 5.3

* Fri Dec  6 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.3-0.1mdk
- Update to gdb 5.2.91, first public snapshot for upcoming gdb 5.3

* Fri Dec  6 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.2.1-3mdk
- Patch1: Fix memory leaks (PR gdb/592, Daniel Jacobowitz)
- Patch2: Use system readline
- Patch11: Add SuSE fix to remove frame pointer on x86-64

* Wed Aug 21 2002 Stew Benedict <sbenedict@mandrakesoft.com> 5.2.1-2mdk
- fix sim build - cjw <cjw@daneel.dyndns.org>

* Mon Aug 19 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.2.1-1mdk
- 5.2.1

* Tue Jun 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.2-3mdk
- Add dwarf2cfi from SuSE release 5.2-31

* Mon Jun 24 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.2-2mdk
- Sanitize specfile
- Merge with SuSE release 5.2-31 (4 new patches):
  - Fix IA-64 breakpoints on L in MLX instruction bundles
  - Add some dwarf2-patches for x86-64
  - Add x86-64 xmm register info
  - Add x86-64 fpregset

* Fri May 17 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.2-1mdk
- 5.2
- Fix versioning
- Sanitize specfile
- Remove Patch0 (threadfpufix), since integrated in upstream sources
- Remove Patch1 (boolfix), since better handled upstream

* Tue May 07 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.1.1-4mdk
- Automated rebuild in gcc3.1 environment

* Tue Feb 26 2002 Stew Benedict <sbenedict@mandrakesoft.com> 5.1.1-3mdk
- gcc295 also provides boolean types - change patch2

* Mon Feb 25 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.1.1-2mdk
- fix build with newer gcc (boolean name clash)

* Mon Feb  4 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.1.1-1mdk
- 5.1.1.

* Wed Jan  9 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.1-3mdk
- Fix some thread+fpu problems (rh).

* Wed Jan 09 2002 David BAUDENS <baudens@mandrakesoft.com> 5.1-2mdk
- Fix menu entry (png icon)

* Tue Dec  4 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.1-1mdk
- 5.1.

* Mon Nov 19 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.0-22mdk
- Fix with new makeinstall.

* Wed Nov 14 2001 Stew Benedict <sbenedict@mandrakesoft.com> 5.0-21mdk
- use CVS like other arches - old tarball doesn't build anymore, and 
- segfault problem seems to have gone away - PPC

* Sat Sep 29 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.0-20mdk
- include the menu file (oops).

* Fri Sep 28 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.0-19mdk
- 20010912 snapshot.

* Fri Sep 14 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.0-17mdk
- Rebuild.

* Fri Sep  7 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.0-16mdk
- s|Linux-Mandrake|Mandrake Linux|;
- 20010813 snapshot.

* Mon Aug  6 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.0-15mdk
- 20010625 snapshot.
- Adjust BuildRequires:

* Fri Jun 15 2001 David BAUDENS <baudens@mandrakesoft.com> 5.0-14mdk
- Use real gdb-5.0 on PPC (or it will segfault every time)

* Sat May 19 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.0-13mdk
- Fix info.
- 20010501 snapshot.

* Mon May 14 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.0-12mdk
- Merge with latest snapshot of rh.

* Thu Mar 15 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.0-11mdk
- New snapshot rh merge.

* Wed Feb 07 2001 Francis Galiegue <fg@mandrakesoft.com> 5.0-10mdk
- Yep, now compiles on ia64

* Tue Feb  6 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.0-9mdk
- Using snapshot 20010119. (should work on ia64 btw).

* Mon Feb 05 2001 Francis Galiegue <fg@mandrakesoft.com> 5.0-8mdk
- ExcludeArch: ia64 - probably 5.1 will integrate it but right now it's not

* Fri Jan 19 2001 David BAUDENS <baudens@mandrakesoft.com> 5.0-7mdk
- Fix a stupid typo in Requires

* Fri Jan 19 2001 David BAUDENS <baudens@mandrakesoft.com> 5.0-6mdk
- Fix build on PPC
- Spec clean up

* Mon Jan 15 2001 David BAUDENS <baudens@mandrakesoft.com> 5.0-5mdk
- BuildRequires: texinfo

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 5.0-4mdk
- automatically added BuildRequires

* Wed Jul 19 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.0-3mdk
- BM

* Wed Jul 05 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.0-2mdk
- merge in rh patches
- add doc files
- added the NEWS file to the %doc files
- don't delete libmmalloc & add it (required by docs in gdb' info pages) :
  we're the only distro to be compliant with this!
- use new macros

* Mon Jun 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.0-1mdk
- new release
- fix source0
- add URL
- make sparc patch only applied when building a sparc rpm (sprc-bldr scks)

* Sat Apr 29 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.18-14mdk
- Set VERSION to version rpm not to cvs date.
- Fix menu post/postun.
- Add all size of icons.

* Thu Apr 27 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.18-13mdk
- Add menu and icon.
- Clean-up specs.
- Adjust groups.
- Back to snapshots 19991004 for glibc-2.1.3.

* Mon Nov 22 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Using cvs snapshot, merging.
- merging with redhat patchs.

* Tue Aug 24 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- thread safe release
