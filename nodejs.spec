Name: nodejs
Version: 0.9.4
Release: 1%{?dist}
Summary: JavaScript runtime
License: MIT and ASL 2.0 and ISC and BSD
Group: Development/Languages
URL: http://nodejs.org/
Source0: http://nodejs.org/dist/v%{version}/node-v%{version}.tar.gz
Source1: macros.nodejs
Source2: nodejs.attr
Source3: nodejs.prov
Source4: nodejs.req
Source5: nodejs-symlink-deps
BuildRequires: v8-devel
BuildRequires: http-parser-devel >= 2.0
BuildRequires: libuv-devel >= %{version}
BuildRequires: c-ares-devel
BuildRequires: zlib-devel
# Node.js requires some features from openssl 1.0.1 for SPDY support
BuildRequires: openssl-devel >= 1:1.0.1

# Exclusive archs must match v8
ExclusiveArch: %{ix86} x86_64 %{arm}

# Node.js currently has a conflict with the 'node' package in Fedora
# The ham-radio group has agreed to rename their binary for us, but
# in the meantime, we're setting an explicit Conflicts: here
Conflicts: node <= 0.3.2-11

# Patches

# This patch is Fedora-specific and allows building the release
# binaries with debugging symbols
Patch0004: 0004-Build-debugging-symbols-by-default.patch

%description
Node.js is a platform built on Chrome's JavaScript runtime
for easily building fast, scalable network applications.
Node.js uses an event-driven, non-blocking I/O model that
makes it lightweight and efficient, perfect for data-intensive
real-time applications that run across distributed devices.

%package docs
Summary: Node.js API documentation
Group: Documentation

%description docs
The API documentation for the Node.js JavaScript runtime.

%prep
%setup -q -n node-v%{version}

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
export CFLAGS='%{optflags}'
export CXXFLAGS='%{optflags}'
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

# own the sitelib directory
mkdir -p %{buildroot}%{_prefix}/lib/node_modules

# install rpm magic
install -Dpm0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/rpm/macros.nodejs
install -Dpm0644 %{SOURCE2} %{buildroot}%{_rpmconfigdir}/fileattrs/nodejs.attr
install -pm0755 %{SOURCE3} %{buildroot}%{_rpmconfigdir}/nodejs.prov
install -pm0755 %{SOURCE4} %{buildroot}%{_rpmconfigdir}/nodejs.req
install -pm0755 %{SOURCE5} %{buildroot}%{_rpmconfigdir}/nodejs-symlink-deps

#install documentation
mkdir -p %{buildroot}%{_defaultdocdir}/%{name}-doc-%{version}/html
cp -pr doc/* %{buildroot}%{_defaultdocdir}/%{name}-doc-%{version}/html
rm -f %{_defaultdocdir}/%{name}-docs-%{version}/html/nodejs.1

%files
%doc ChangeLog LICENSE README.md AUTHORS
%{_bindir}/node
%{_mandir}/man1/node.*
%{_rpmconfigdir}/fileattrs/nodejs.attr
%{_rpmconfigdir}/nodejs*
%dir %{_prefix}/lib/node_modules

%files docs
%{_defaultdocdir}/%{name}-docs-%{version}
%doc LICENSE

%changelog
* Wed Dec 26 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.4-1
- new upstream release 0.9.4
- system library patches are now upstream
- respect optflags
- include documentation in subpackage
- add RPM dependency generation and related magic
- guard libuv depedency so it always gets bumped when nodejs does

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

