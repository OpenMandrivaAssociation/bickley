%define major           0
%define libname         %mklibname %{name} %{major}
%define develname       %mklibname %{name} -d

%define version 0.4
%define rel 2
%define snapshot git20090814
%define release %mkrel 0.%{snapshot}.%{rel}

%define sversion %{version}%{snapshot}

Name: bickley
Summary: Bickley is a meta data management API and framework
Group: Graphical desktop/Other
Version: %{version}
License: LGPLv2.1
URL: http://www.moblin.org
Release: %{release}
Source0: %{name}-%{sversion}.tar.gz 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

# patches from fedora team
Patch0: nocrash.patch
Patch1: bickley-0.4.3-kozo-format.patch
Patch2: 0001-Port-to-gupnp-0.13.patch

BuildRequires: libglib2-devel
BuildRequires: libdbus-glib-devel
BuildRequires: clutter-gst-devel
BuildRequires: libgstreamer-devel
BuildRequires: libexif-devel
BuildRequires: libmesagl-devel
BuildRequires: gupnp-devel
BuildRequires: libgupnp-av-devel
BuildRequires: tdb-devel
BuildRequires: libGConf2-devel
BuildRequires: libogg-devel
BuildRequires: libvorbis-devel
BuildRequires: libid3tag-devel
BuildRequires: libflac-devel
BuildRequires: python

Requires: libclutter-gtk0.10_0
Requires: gstreamer
Requires: sqlite-tools
Requires: xdg-user-dirs

%description
Bickley is a meta data management API and framework. The core API allows 
storing and querying of URIs and associating key/value pairs. The core bickley
API in the libbickley library provides shared access to common meta-data
storage. Different processes can access and manipulate the same set of URIs and
meta data about them in parallel

%package -n %{libname}
Summary: Bickley is a meta data management API and framework
Group: System/Libraries

%description -n %{libname}
Bickley is a meta data management API and framework

%package -n libkozo%{major}
Summary: Kozo library from Bickley (a meta data management API and framework)
Group: System/Libraries

%description -n libkozo%{major}
Kozo library from Bickley (a meta data management API and framework)

%package -n %{develname}
Summary: Bickley development environment
Group: Development/C

Requires: %{libname} = %{version}-%{release}
Provides: %{name}-devel

%description -n %{develname}
Development headers and libraries for Bickley

%prep
%setup -q -n %{name}-%{sversion}
%patch0 -p1
%patch1 -p0
%patch2 -p1
perl -pi -e 's,^./configure.*,,' ./autogen.sh

%build
./autogen.sh
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%clean
rm -rf %{buildroot}

%pre -n %{name}
if [ "$1" -gt 1 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule \
    %{_sysconfdir}/gconf/schemas/bkl-orbiter.schemas \
    > /dev/null || :
fi

%preun -n %{name}
if [ "$1" -gt 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule \
    %{_sysconfdir}/gconf/schemas/bkl-orbiter.schemas \
    > /dev/null || :
fi

%post -n %{name}
/sbin/ldconfig
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
    %{_sysconfdir}/gconf/schemas/bkl-orbiter.schemas \
  > /dev/null || :

%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/libbickley*.so.*

%files -n %{name}
%doc COPYING.LIB AUTHORS NEWS README ChangeLog
%{_sysconfdir}/gconf/schemas/bkl-orbiter.schemas
%{_sysconfdir}/xdg/autostart/bkl-orbiter.desktop
%{_datadir}/dbus-1/services/org.moblin.Bickley.Investigator.service
%{_datadir}/dbus-1/services/org.moblin.Bickley.Orbiter.service
%{_libexecdir}/bkl-investigator
%{_bindir}/bkl-orbiter
%{_bindir}/bkl-source-test
%{_bindir}/bkl-client-test
%{_bindir}/bkl-rename-user

%files -n libkozo%{major}
%{_libdir}/libkozo*.so.*

%files -n %{develname}
%defattr(-,root,root,-)
%{_includedir}/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/lib*.a
