%global srcname pymssql
%global sum Python3 MSSQL Client
# this shortcut overwrites what is usally a macro, but it is required due to lack of EPEL's srpm macros in debian
%global python3_pkgversion 38
Summary: %{sum}
Name: pymssql
Packager: Wolfgang Glas <wolfgang.glas@iteg.at>
Version: 2.1.5
Release: 0
License: Apache License 2.0
Group: Development/Libraries
Source: pymssql-%{version}.tar.gz
BuildRequires: gcc
BuildRequires: git
BuildRequires: freetds-devel
BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: python%{python3_pkgversion}-rpm-macros
BuildRequires: python%{python3_pkgversion}-setuptools
BuildRequires: python%{python3_pkgversion}-Cython
BuildRoot: /var/tmp/%{name}-buildroot
###XBCS-PBA-Category: pytools
###XBCS-PBA-Generation: 1
###XBCS-PBA-Distributions: centos8
###XBCS-PBA-Repository: rpm.clazzes.org
###XBCS-PBA-Build-Source-pba: http://rpm.clazzes.org/repos/pba-1.0/pba-1.0.repo
# epel-release should be installed in all centos8 tarballs
# based on
#   https://fedoraproject.org/wiki/Packaging:Python
#   https://fedoraproject.org/wiki/PackagingDrafts:Python3EPEL

%description
%{sum}

%package -n python%{python3_pkgversion}-%{srcname}
Requires: python%{python3_pkgversion}
Requires: freetds-libs
Summary: %{sum}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%description -n python%{python3_pkgversion}-%{srcname}
%{sum}

%prep
%autosetup

%build
%py3_build

%install
%py3_install

%check
#%{__python3} setup.py test

%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitearch}/*

%changelog
