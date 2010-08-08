#!/bin/bash -x

# Get metadata
pyver=2.6
architecture="i386";
pybin="python${pyver}";
ver=$(${pybin} setup.py --version);
package=$(${pybin} setup.py --name);
required="${pybin} (>=${pyver})"
req=$(${pybin} setup.py --requires);
if [ -n "$req" ]; then
required=$(echo "${required}, python-${req}" | sed -n '1h;2,$H;${g;s/\n/, python-/g;p}');
fi
author=$(${pybin} setup.py --author);
authoremail=$(${pybin} setup.py --author-email);
maintainer=$(${pybin} setup.py --maintainer);
maintaineremail=$(${pybin} setup.py --maintainer-email);
sdescription=$(${pybin} setup.py --description);
ldescription=$(${pybin} setup.py --long-description);
url=$(${pybin} setup.py --url);
description=$(echo -e "${sdescription}\n${ldescription}");
if [ "$url" != "UNKNOWN" ]; then
description=$(echo -e "${description}\n ${url}");
fi
# Clean
rm -r build
#rm ./docs/*~
${pybin} setup.py clean

# Build
${pybin} setup.py build

# Fake install
${pybin} setup.py install --root dist/deb
cd dist

# Get installed size
fss=$(du -s deb)
set -- $fss
fs=$1

# Create Deb control file
mkdir -p deb/DEBIAN
control="./deb/DEBIAN/control"
touch "${control}" 2> /dev/null
if [ -e "${control}" ] ; then
  echo "Package: python-${package}" > "${control}"
  echo "Version: ${ver}" >> "${control}"
  echo "Maintainer: ${maintainer} <${maintaineremail}>" >> "${control}"
  echo "Installed-Size: ${fs}" >> "${control}"
  echo "Architecture: ${architecture}" >> "${control}"
  echo "Depends: ${required}" >> "${control}"
  echo "Description: ${description}" >> "${control}"
fi

## Copy documentation
#mkdir -p deb/usr/share/doc/$package
#cp ../docs/* deb/usr/share/doc/$package

# Make deb package
deb="${package}-${ver}-py${pyver}-${architecture}.deb"
dpkg-deb -b deb ${deb}
rm -r deb

cd ..

# Clean
rm -r build
rm -r ${package}.egg-info

# Make source & egg distributions
#python setup.py sdist --formats zip,gztar
#python setup.py bdist_egg

#ftp -n $hostname <<EOF
#quote USER $username
#quote PASS $password
#prompt
#passive
#binary
#lcd ./dist
#cd /public_html/packages
#put ${deb}
#quit
#EOF
