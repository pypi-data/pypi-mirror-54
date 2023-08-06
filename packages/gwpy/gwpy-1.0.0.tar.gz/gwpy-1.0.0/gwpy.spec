# vim:set ft=spec:
#
# -- global settings ----------------------------------------------------------

%global srcname gwpy

Name:           python-%{srcname}
Version:        1.0.0
Release:        1%{?dist}
Summary:        A python package for gravitational-wave astrophysics

License:        GPLv3+
URL:            https://github.com/gwpy/gwpy
Source0:        https://files.pythonhosted.org/packages/source/g/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  rpm-build
BuildRequires:  python-rpm-macros
BuildRequires:  python2-rpm-macros
BuildRequires:  python2-setuptools

%description
GWpy is a collaboration-driven Python package providing tools for
studying data from ground-based gravitational-wave detectors.

GWpy provides a user-friendly, intuitive interface to the common
time-domain and frequency-domain data produced by the LIGO and Virgo
observatories and their analyses, with easy-to-follow tutorials at each
step.

<https://gwpy.github.io>

# Release status

[![PyPI version](https://badge.fury.io/py/gwpy.svg)](http://badge.fury.io/py/gwpy)
[![Conda version](https://img.shields.io/conda/vn/conda-forge/gwpy.svg)](https://anaconda.org/conda-forge/gwpy/)

[![DOI](https://zenodo.org/badge/9979119.svg)](https://zenodo.org/badge/latestdoi/9979119)
[![License](https://img.shields.io/pypi/l/gwpy.svg)](https://choosealicense.com/licenses/gpl-3.0/)
![Supported Python versions](https://img.shields.io/pypi/pyversions/gwpy.svg)

# Development status

[![Linux](https://img.shields.io/circleci/project/github/gwpy/gwpy/master.svg?label=Linux)](https://circleci.com/gh/gwpy/gwpy)
[![OSX](https://img.shields.io/travis/gwpy/gwpy/master.svg?label=macOS)](https://travis-ci.com/gwpy/gwpy)
[![Windows](https://img.shields.io/appveyor/ci/gwpy/gwpy/master.svg?label=Windows)](https://ci.appveyor.com/project/gwpy/gwpy/branch/master)
[![codecov](https://codecov.io/gh/gwpy/gwpy/branch/master/graph/badge.svg)](https://codecov.io/gh/gwpy/gwpy)
[![Maintainability](https://api.codeclimate.com/v1/badges/2cf14445b3e070133745/maintainability)](https://codeclimate.com/github/gwpy/gwpy/maintainability)

# Installation

To install, you can do:

```
conda install -c conda-forge gwpy
```

or

```
python -m pip install gwpy
```

You can test your installation, and its version by

```
python -c "import gwpy; print(gwpy.__version__)"
```

# License

GWpy is released under the GNU General Public License v3.0 or later, see [here](https://choosealicense.com/licenses/gpl-3.0/) for a description of this license, or see the [LICENSE](https://github.com/gwpy/gwpy/blob/master/LICENSE) file for the full text.


# -- python2-gwpy -------------------------------------------------------------

%package -n python2-%{srcname}
Summary:        %{summary}
Requires:       python-six >= 1.5
Requires:       python-dateutil
Requires:       python-enum34
Requires:       numpy >= 1.7.1
Requires:       scipy >= 0.12.1
Requires:       python-matplotlib >= 1.2.0
Requires:       python-astropy >= 1.1.1
Requires:       h5py >= 1.3
Requires:       python2-ldas-tools-framecpp >= 2.6.0
Requires:       python2-lal >= 6.14.0
Requires:       python2-ligo-segments >= 1.0.0
Requires:       python-pathlib
Requires:       python2-tqdm >= 4.10.0
Requires:       python2-gwosc
Requires:       python2-dqsegdb2
Requires:       python2-gwdatafind

%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
GWpy is a collaboration-driven Python package providing tools for
studying data from ground-based gravitational-wave detectors.

GWpy provides a user-friendly, intuitive interface to the common
time-domain and frequency-domain data produced by the LIGO and Virgo
observatories and their analyses, with easy-to-follow tutorials at each
step.

<https://gwpy.github.io>

# Release status

[![PyPI version](https://badge.fury.io/py/gwpy.svg)](http://badge.fury.io/py/gwpy)
[![Conda version](https://img.shields.io/conda/vn/conda-forge/gwpy.svg)](https://anaconda.org/conda-forge/gwpy/)

[![DOI](https://zenodo.org/badge/9979119.svg)](https://zenodo.org/badge/latestdoi/9979119)
[![License](https://img.shields.io/pypi/l/gwpy.svg)](https://choosealicense.com/licenses/gpl-3.0/)
![Supported Python versions](https://img.shields.io/pypi/pyversions/gwpy.svg)

# Development status

[![Linux](https://img.shields.io/circleci/project/github/gwpy/gwpy/master.svg?label=Linux)](https://circleci.com/gh/gwpy/gwpy)
[![OSX](https://img.shields.io/travis/gwpy/gwpy/master.svg?label=macOS)](https://travis-ci.com/gwpy/gwpy)
[![Windows](https://img.shields.io/appveyor/ci/gwpy/gwpy/master.svg?label=Windows)](https://ci.appveyor.com/project/gwpy/gwpy/branch/master)
[![codecov](https://codecov.io/gh/gwpy/gwpy/branch/master/graph/badge.svg)](https://codecov.io/gh/gwpy/gwpy)
[![Maintainability](https://api.codeclimate.com/v1/badges/2cf14445b3e070133745/maintainability)](https://codeclimate.com/github/gwpy/gwpy/maintainability)

# Installation

To install, you can do:

```
conda install -c conda-forge gwpy
```

or

```
python -m pip install gwpy
```

You can test your installation, and its version by

```
python -c "import gwpy; print(gwpy.__version__)"
```

# License

GWpy is released under the GNU General Public License v3.0 or later, see [here](https://choosealicense.com/licenses/gpl-3.0/) for a description of this license, or see the [LICENSE](https://github.com/gwpy/gwpy/blob/master/LICENSE) file for the full text.

# -- build stages -------------------------------------------------------------

%prep
%autosetup -n %{srcname}-%{version}

%build
%py2_build

%install
%py2_install

# -- files --------------------------------------------------------------------

%files -n python2-%{srcname}
%license LICENSE
%doc README.md
%{python2_sitelib}/*
%{_bindir}/gwpy-plot

# -- changelog ----------------------------------------------------------------

%changelog
* Tue Oct 29 2019 Duncan Macleod <duncan.macleod@ligo.org> - 1.0.0-1
- GWpy-1.0.0

* Wed Apr 24 2019 Duncan Macleod <duncan.macleod@ligo.org> - 0.15.0-1
- GWpy-0.15.0

* Fri Mar 22 2019 Duncan Macleod <duncan.macleod@ligo.org> - 0.14.2-1
- GWpy-0.14.2

* Wed Mar 13 2019 Duncan Macleod <duncan.macleod@ligo.org> - 0.14.1-1
- GWpy-0.14.1

* Thu Feb 28 2019 Duncan Macleod <duncan.macleod@ligo.org> - 0.14.0-1
- GWpy-0.14.0

* Tue Feb 05 2019 Duncan Macleod <duncan.macleod@ligo.org> - 0.13.1-1
- 0.13.1

* Tue Feb 05 2019 Duncan Macleod <duncan.macleod@ligo.org> - 0.13.0-1
- 0.13.0

* Wed Sep 19 2018 Duncan Macleod <duncan.macleod@ligo.org> - 0.12.2-1
- 0.12.2: bug-fix relase for gwpy-0.12

* Wed Sep 19 2018 Duncan Macleod <duncan.macleod@ligo.org> - 0.12.1-1
- 0.12.1: bug-fix release for gwpy-0.12

* Thu Aug 16 2018 Duncan Macleod <duncan.macleod@ligo.org> - 0.12.0-1
- 0.12.0: development release of GWpy

* Fri Jun 15 2018 Duncan Macleod <duncan.macleod@ligo.org> - 0.11.0-1
- 0.11.0: development release of GWpy

* Thu Apr 19 2018 Duncan Macleod <duncan.macleod@ligo.org> - 0.10.1-1
- 0.10.1: bug-fix for gwpy-0.10

* Thu Apr 19 2018 Duncan Macleod <duncan.macleod@ligo.org> - 0.10.0-1
- 0.10.0: development release of GWpy

* Sat Mar 24 2018 Duncan Macleod <duncan.macleod@ligo.org> - 0.9.0-1
- 0.9.0: development release of GWpy

* Mon Feb 19 2018 Duncan Macleod <duncan.macleod@ligo.org> - 0.8.1-1
- 0.8.1: bug-fix for gwpy-0.8

* Sun Feb 18 2018 Duncan Macleod <duncan.macleod@ligo.org> - 0.8.0-1
- 0.8.0: development release of GWpy

* Thu Jan 25 2018 Duncan Macleod <duncan.macleod@ligo.org> - 0.7.5-1
- 0.7.5: packaging bug-fix for gwpy-0.7

* Thu Jan 25 2018 Duncan Macleod <duncan.macleod@ligo.org> - 0.7.4-1
- 0.7.4: packaging bug-fix for gwpy-0.7

* Wed Jan 24 2018 Duncan Macleod <duncan.macleod@ligo.org> - 0.7.3-1
- 0.7.3: bug fix release for gwpy-0.7

* Wed Jan 24 2018 Duncan Macleod <duncan.macleod@ligo.org> - 0.7.2-1
- 0.7.2: bug fix release for gwpy-0.7

* Mon Jan 22 2018 Duncan Macleod <duncan.macleod@ligo.org> - 0.7.1-1
- 0.7.1

* Fri Jan 19 2018 Duncan Macleod <duncan.macleod@ligo.org> - 0.7.0-1
- 0.7.0

* Thu Oct 12 2017 Duncan Macleod <duncan.macleod@ligo.org> - 0.6.2-1
- 0.6.2

* Tue Aug 29 2017 Duncan Macleod <duncan.macleod@ligo.org> - 0.6.1-1
- 0.6.1 release

* Fri Aug 18 2017 Duncan Macleod <duncan.macleod@ligo.org> - 0.6-1
- 0.6 release

* Wed May 24 2017 Duncan Macleod <duncan.macleod@ligo.org> - 0.5.2-1
- 0.5.2

