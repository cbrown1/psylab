#!/bin/bash -x

# Set these as needed
pyver=2.6
architecture="all"; #"i386";
section='python';  # Most python packages seem to go here
pybin="python${pyver}";

# Get metadata
ver=$(${pybin} setup.py --version);
package=$(${pybin} setup.py --name);
required="${pybin} (>=${pyver})"        # Require the python version being used
req=$(${pybin} setup.py --requires);    # Look for package-specific requires
if [ -n "$req" ]; then                  # prepend with 'python-' and add to list
    required=$(echo "${required}, python-${req}" | sed -n '1h;2,$H;${g;s/\n/, python-/g;p}');
fi
author=$(${pybin} setup.py --author);
authoremail=$(${pybin} setup.py --author-email);
maintainer=$(${pybin} setup.py --maintainer);
maintaineremail=$(${pybin} setup.py --maintainer-email);
sdescription=$(${pybin} setup.py --description);      # Build deb description from py short desc
ldescription=$(${pybin} setup.py --long-description); # and py long desc
url=$(${pybin} setup.py --url);
description=$(echo -e "${sdescription}\n${ldescription}"); # Add url to end of desc if present
if [ "$url" != "UNKNOWN" ]; then
description=$(echo -e "${description}\n .\n ${url}");
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

cd deb

# Create Deb control file
mkdir -p DEBIAN
control="./DEBIAN/control"
touch "${control}" 2> /dev/null
if [ -e "${control}" ] ; then
  echo "Package: python-${package}" > "${control}"
  echo "Version: ${ver}" >> "${control}"
  if [ "$url" != "UNKNOWN" ]; then
    echo "Homepage: ${url}" >> "${control}"
  fi
  echo "Maintainer: ${maintainer} <${maintaineremail}>" >> "${control}"
  echo "Installed-Size: ${fs}" >> "${control}"
  echo "Section: ${section}" >> "${control}"
  echo "Architecture: ${architecture}" >> "${control}"
  echo "Depends: ${required}" >> "${control}"
  echo "Description: ${description}" >> "${control}"
fi

md5sum `find . -type f | grep -v '^[.]/DEBIAN/'  | sed -e 's/.\///'` >DEBIAN/md5sums

cd ..

## Copy documentation
#mkdir -p deb/usr/share/doc/$package
#cp ../docs/* deb/usr/share/doc/$package

# Make deb package
deb="${package}_${ver}_${architecture}.deb"
dpkg-deb -b deb ${deb}

rm -r deb
cd ..

# Clean
rm -r build
rm -r ${package}.egg-info

# Make source & egg distributions
#python setup.py sdist --formats zip,gztar
#python setup.py bdist_egg

# Upload
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