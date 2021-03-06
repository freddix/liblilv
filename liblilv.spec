Summary:	Library to use with LV2 plugins
Name:		liblilv
Version:	0.20.0
Release:	1
License:	GPL v2
Group:		Libraries
Source0:	http://download.drobilla.net/lilv-%{version}.tar.bz2
# Source0-md5:	f88419fa70cc96dfdc7e0bf3cd09b180
BuildRequires:	glib-devel
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	libsord-devel >= 0.12.2
BuildRequires:	libsratom-devel >= 0.4.6
BuildRequires:	lv2-devel >= 1.10.0
BuildRequires:	pkg-config
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lilv is a library to make the use of LV2 plugins as simple as possible
for applications. Lilv is the successor to SLV2, rewritten to be
significantly faster and have minimal dependencies.

%package devel
Summary:	Header files for lilv library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This is the package containing the header files for lilv library.

%package progs
Summary:	Tools included in lilv library
Group:		Applications
Requires:	%{name} = %{version}-%{release}

%description progs
Tools included in lilv library.

%prep
%setup -qn lilv-%{version}

sed -i "s|bld.add_post_fun(autowaf.run_ldconfig)||" wscript

%build
export CC="%{__cc}"
export CXX="%{__cxx}"
export CCFLAGS="%{rpmcflags}"
export CXXFLAGS="%{rpmcxxflags}"
export LDFLAGS="%{rpmldflags}"
./waf configure \
	--libdir=%{_libdir}	\
	--mandir=%{_mandir}	\
	--prefix=%{_prefix}	\
	--nocache
./waf -v

%install
rm -rf $RPM_BUILD_ROOT

./waf -v install	\
	--destdir=$RPM_BUILD_ROOT

chmod +x $RPM_BUILD_ROOT%{_libdir}/*.so*

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/liblilv-0.so.?
%attr(755,root,root) %{_libdir}/liblilv-0.so.*.*.*
%{_mandir}/man1/lv2info.1*
%{_mandir}/man1/lv2ls.1*

%files progs
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/lilv-bench
%attr(755,root,root) %{_bindir}/lv2bench
%attr(755,root,root) %{_bindir}/lv2info
%attr(755,root,root) %{_bindir}/lv2ls

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblilv-0.so
%{_includedir}/lilv-0
%{_pkgconfigdir}/lilv-0.pc

