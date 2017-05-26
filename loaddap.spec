Summary:	The OPeNDAP Matlab Command Line Interface Client
Summary(pl.UTF-8):	Klient linii poleceń Matlaba do OPeNDAP
Name:		loaddap
Version:	3.7.3
Release:	4
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://www.opendap.org/pub/source/%{name}-%{version}.tar.gz
# Source0-md5:	9482c748418c38c6e26a2b63dfd5643b
#Patch0:		%{name}-libdap.patch
Patch0:		%{name}-includes.patch
Patch1:		%{name}-octave.patch
URL:		http://opendap.org/
BuildRequires:	autoconf >= 2.68
BuildRequires:	automake
BuildRequires:	libdap-devel >= 3.12.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	octave-devel
BuildRequires:	pkgconfig
Requires:	libdap >= 3.12.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		octave_m_dir	%(octave-config --m-site-dir)
%define		octave_oct_dir	%(octave-config --oct-site-dir)

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
	MEX=/usr/bin/mkoctfile \
	MEXEXT=oct \
	--with-matlab=/usr
%{__make} \
	MEX="/usr/bin/mkoctfile -I. -DHAVE_CONFIG_H -I/usr/include/octave" \
	MEXFLAGS= \
	MEXLDADD=

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{octave_m_dir},%{octave_oct_dir}}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/*.oct $RPM_BUILD_ROOT%{octave_oct_dir}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/*.m $RPM_BUILD_ROOT%{octave_m_dir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYRIGHT_URI ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/writedap
%attr(755,root,root) %{octave_oct_dir}/loaddap.oct
%{octave_m_dir}/loaddap.m
%{octave_m_dir}/whodap.m
