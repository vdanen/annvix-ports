#!/bin/sh
#
# $Id$

if [ "`whoami`" == "root" ]; then
    echo "Do not build ports as root!  Aborting."
    exit 1
fi

SPEC="tree.spec"
MD5SUM=93110789bcd48f633c2ea1d1b3835dac
ARCH=`rpm --eval %_target_cpu`
PTREE="/usr/local/ports/packages"

if [ ! -f $SPEC ]; then
    echo "spec file $SPEC is missing.. please update your ports directory.  Aborting."
    exit 1
fi

NAME="`egrep '^%define name' $SPEC|cut -f 2`"
VERSION="`egrep '^%define version' $SPEC|cut -f 2`"
RELEASE="`egrep '^%define release' $SPEC|cut -f 2`"
SOURCEFILE="`egrep '^Source:' $SPEC|cut -f 3|sed s/%{name}/$NAME/|sed s/%{version}/$VERSION/`"
SOURCE=`basename $SOURCEFILE`

# only download source files if they don't exist locally
if [ ! -f $SOURCE ]; then
    curl -O $SOURCEFILE
fi

if [ ! -f $SOURCE ]; then
    echo "Unable to download source file: $SOURCEFILE.  Aborting."
    exit 1
fi

md5=`md5sum $SOURCE|cut -f 1 -d ' '`

if [ "$md5" != "$MD5SUM" ]; then
    echo "md5sums do not match!  Possible trojan file?  Aborting."
    exit 1
fi

pwd=`pwd`

rm -rf {tmp,BUILD,SRPMS,RPMS}
mkdir -p {tmp,BUILD,SRPMS,RPMS/{$ARCH,noarch}}
for i in `egrep '^Patch' $SPEC|cut -f 3`
do
    if [ ! -f $i ]; then
	echo "patch file $i is missing... please update your ports directory.  Aborting."
	exit 1
    fi
done

rpm -ba $SPEC --clean --define="_topdir $pwd" --define="_tmppath $pwd/tmp" --define="_sourcedir $pwd"

mv -f RPMS/*/*.rpm $PTREE/RPMS
mv -f SRPMS/*.rpm $PTREE/SRPMS
pushd $PTREE
genhdlist RPMS
popd

rm -rf {tmp,BUILD,SRPMS,RPMS}
