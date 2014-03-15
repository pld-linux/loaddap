# TODO: proper paths for .oct and *.m files
Summary:	The OPeNDAP Matlab Command Line Interface Client
Summary(pl.UTF-8):	Klient linii poleceń Matlaba do OPeNDAP
Name:		loaddap
Version:	3.7.2
Release:	0.1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://www.opendap.org/pub/source/%{name}-%{version}.tar.gz
# Source0-md5:	121330c1568f00e6861d82d15492d3de
Patch0:		%{name}-libdap.patch
Patch1:		%{name}-includes.patch
URL:		http://opendap.org/
BuildRequires:	autoconf >= 2.68
BuildRequires:	automake
BuildRequires:	libdap-devel >= 3.8.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	octave-devel
BuildRequires:	pkgconfig
Requires:	libdap >= 3.8.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the OPeNDAP Matlab command line interface
client. This client can be used to read data from DAP2-compilant
servers directly into Matlab/Octave.

%description -l pl.UTF-8
Ten pakiet zawiera klienta linii poleceń Matlaba do OPeNDAP. Można
go używać do odczytu danych z serwerów zgodnych z DAP2 bezpośrednio
do Matlaba/Octave.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%{__sed} -i -e 's,/extern/include,/include/octave,' conf/matlab.m4

%build
%{__libtoolize}
%{__aclocal} -I conf
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	MATLAB_VERSION=7.8 \
	MEX=/usr/bin/mkoctfile \
	MEXEXT=oct \
	--with-matlab=/usr
%{__make} \
	MEX="/usr/bin/mkoctfile -I. -DHAVE_CONFIG_H" \
	MEXFLAGS=

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYRIGHT_URI ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/writedap
# FIXME: proper location for .oct and .m files
%attr(755,root,root) %{_bindir}/loaddap.oct
%{_bindir}/loaddap.m
%{_bindir}/whodap.m
