%global srcname pkginfo
%global sum Query metadata from sdists / bdists / installed packages

Name:           python-%{srcname}
Version:        1.4.2
Release:        1%{?dist}
Summary:        %{sum}

# License is missing from the source repo: see https://bugs.launchpad.net/pkginfo/+bug/1591344
License:        Python
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        https://pypi.python.org/packages/39/c9/111ececbeed8e69cd1b6bec79a32a0b0f6074038a4244e58e285ad278248/pkginfo-1.4.2.tar.gz
# Upstream installs the test package, and we don't need to distribute that.
Patch0:         0001-Stop-installing-the-test-package.patch

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-nose
BuildRequires:  python-sphinx


%description
This package provides an API for querying the distutils metadata written in the
PKG-INFO file inside a source distribution (an sdist) or a binary distribution
(e.g., created by running bdist_egg). It can also query the EGG-INFO directory
of an installed distribution, and the *.egg-info stored in a "development
checkout" (e.g, created by running setup.py develop).


%package -n python2-%{srcname}
Summary:        %{sum}
Requires:       python-setuptools
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
This package provides an API for querying the distutils metadata written in the
PKG-INFO file inside a source distribution (an sdist) or a binary distribution
(e.g., created by running bdist_egg). It can also query the EGG-INFO directory
of an installed distribution, and the *.egg-info stored in a "development
checkout" (e.g, created by running setup.py develop).


%package -n python-%{srcname}-doc
Summary:        Documentation for the python-%{srcname} packages

%description -n python-%{srcname}-doc
This package provides documentation for the Python pkginfo package. pkginfo
provides an API for querying the distutils metadata written in the PKG-INFO
file inside a source distribution (an sdist) or a binary distribution (e.g.,
created by running bdist_egg). It can also query the EGG-INFO directory of an
installed distribution, and the *.egg-info stored in a "development checkout"
(e.g, created by running setup.py develop).


%prep
%autosetup -p1 -n %{srcname}-%{version}
rm -rf *.egg-info


%build
%{__python2} setup.py build

cd docs
make %{?_smp_mflags} html
rm .build/html/objects.inv

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

ln -s %{_bindir}/pkginfo %{buildroot}%{_bindir}/pkginfo-2.7
ln -s %{_bindir}/pkginfo-2.7 %{buildroot}%{_bindir}/pkginfo-2


# Upstream ships a broken unit test: see https://bugs.launchpad.net/pkginfo/+bug/1591298
# Until that's fixed, skip testing.


%files -n python2-%{srcname}
%doc README.txt CHANGES.txt
%{python2_sitelib}/*
%{_bindir}/pkginfo
%{_bindir}/pkginfo-2
%{_bindir}/pkginfo-2.7

%files -n python-%{srcname}-doc
%doc README.txt CHANGES.txt
%doc docs/.build/html/*

%changelog
* Wed Apr 04 2018 Tristan Cacqueray <tdecacqu@redhat.com> - 1.4.2-1
- Bump to 1.4.2 release

* Thu Jun 09 2016 Jeremy Cline <jeremy@jcline.org> - 1.6.5-1
- Initial commit
