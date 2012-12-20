Name: nodejs
Version: 0.9.3
Release: 9%{?dist}
Summary: JavaScript runtime
License: MIT and ASL 2.0 and ISC and BSD
Group: Development/Languages
URL: http://nodejs.org/
Source0: http://nodejs.org/dist/v%{version}/node-v%{version}.tar.gz
BuildRequires: v8-devel
BuildRequires: http-parser-devel >= 2.0
BuildRequires: libuv-devel
BuildRequires: c-ares-devel
BuildRequires: zlib-devel
# Node.js requires some features from openssl 1.0.1 for SPDY support
BuildRequires: openssl-devel

# Exclusive archs must match v8
ExclusiveArch: %{ix86} x86_64 %{arm}

# Node.js currently has a conflict with the 'node' package in Fedora
# The ham-radio group has agreed to rename their binary for us, but
# in the meantime, we're setting an explicit Conflicts: here
Conflicts: node <= 0.3.2-11

# Patches

# The following patches have been accepted upstream and can
# be removed once node.js 0.9.4 is released
Patch0001: 0001-build-allow-linking-against-system-http_parser.patch
Patch0002: 0002-build-allow-linking-against-system-c-ares.patch
Patch0003: 0003-build-allow-linking-against-system-libuv.patch

# This patch is Fedora-specific and allows building the release
# binaries with debugging symbols
Patch0004: 0004-Build-debugging-symbols-by-default.patch

%description
Node.js is a platform built on Chrome's JavaScript runtime
for easily building fast, scalable network applications.
Node.js uses an event-driven, non-blocking I/O model that
makes it lightweight and efficient, perfect for data-intensive
real-time applications that run across distributed devices.


%prep
%setup -q -n node-v%{version}

%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1

# Make sure nothing gets included from bundled deps:
# We only delete the source and header files, because
# the remaining build scripts are still used.

find deps/cares -name "*.c" -exec rm -f {} \;
find deps/cares -name "*.h" -exec rm -f {} \;

find deps/npm -name "*.c" -exec rm -f {} \;
find deps/npm -name "*.h" -exec rm -f {} \;

find deps/zlib -name "*.c" -exec rm -f {} \;
find deps/zlib -name "*.h" -exec rm -f {} \;

find deps/v8 -name "*.c" -exec rm -f {} \;
find deps/v8 -name "*.h" -exec rm -f {} \;

find deps/http_parser -name "*.c" -exec rm -f {} \;
find deps/http_parser -name "*.h" -exec rm -f {} \;

find deps/openssl -name "*.c" -exec rm -f {} \;
find deps/openssl -name "*.h" -exec rm -f {} \;

find deps/uv -name "*.c" -exec rm -f {} \;
find deps/uv -name "*.h" -exec rm -f {} \;

%build
./configure --prefix=%{_prefix} \
           --shared-v8 \
           --shared-openssl \
           --shared-zlib \
           --shared-cares \
           --shared-libuv \
           --shared-http-parser \
           --without-npm \
           --without-dtrace
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

%make_install INSTALL='install -p'

# and remove dtrace file again
rm -rf %{buildroot}/%{_prefix}/lib/dtrace

# Set the binary permissions properly
chmod 0755 %{buildroot}/%{_bindir}/node

%files
%doc ChangeLog LICENSE README.md AUTHORS
%{_bindir}/node
%{_mandir}/man1/node.*

%changelog
* Thu Dec 20 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.9.3-9
- Drop requirement on openssl 1.0.1

* Wed Dec 19 2012 Dan Horák <dan[at]danny.cz> - 0.9.3-8
- set exclusive arch list to match v8

* Tue Dec 18 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.9.3-7
- Add remaining changes from code review
- Remove unnecessary BuildRequires on findutils
- Remove %%clean section

* Fri Dec 14 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.9.3-6
- Fixes from code review
- Fix executable permissions
- Correct the License field
- Build debuginfo properly

* Thu Dec 13 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.9.3-5
- Return back to using the standard binary name
- Temporarily adding a conflict against the ham radio node package until they
  complete an agreed rename of their binary.

* Wed Nov 28 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.9.3-4
- Rename binary and manpage to nodejs

* Mon Nov 19 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.9.3-3
- Update to latest upstream development release 0.9.3
- Include upstreamed patches to unbundle dependent libraries

* Tue Oct 23 2012 Adrian Alves <alvesadrian@fedoraproject.org>  0.8.12-1
- Fixes and Patches suggested by Matthias Runge

* Mon Apr 09 2012 Adrian Alves <alvesadrian@fedoraproject.org> 0.6.5
- First build.

