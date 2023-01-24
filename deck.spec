%define         pkgname         deck
%global         forgeurl        https://github.com/Kong/%{pkgname}
%global 	debug_package %{nil}
%define 	_build_id_links none

Name:		%{pkgname}
Version:        1.17.2
Release:	1%{?dist}
License:	Apache License v2.0
Vendor:		Kong Inc.
URL:		%{forgeurl}
Source0:	https://github.com/Kong/%{pkgname}/releases/download/v%{version}/v%{version}.tar.gz
#Patch0:		patch.gopsutil.version.patch
Summary: 	Declarative configuration for Kong

BuildRequires:  golang git

%description 
Declarative configuration for Kong

%prep
%autosetup

%setup
#%patch0 -p1

%build
go build

%install
install -Dpm 0755 %{pkgname} %{buildroot}%{_bindir}/%{pkgname}

%files
%{_bindir}/deck

%changelog
* Tue Jan 24 2023 Udo Seidel <udoseidel@gmx.de> 1.17.2-1
- a lot of bumping of versions of different components
- full changelog is here: https://github.com/Kong/deck/blob/main/CHANGELOG.md

* Thu Dec 22 2022 Udo Seidel <udoseidel@gmx.de> 1.17.1-1
- Update go-kong to fix a bug causing wrong injection of defaults for arbitrary map fields. (https://github.com/Kong/go-kong/pull/258)

* Thu Dec 22 2022 Udo Seidel <udoseidel@gmx.de> 1.17.0-1
- version update
- added patch for fedora builds
- full changelog is here: https://github.com/Kong/deck/blob/main/CHANGELOG.md

* Sun Nov 13 2022 Udo Seidel <udoseidel@gmx.de> 1.16.1-2
- Fix issue with ping when running against Konnect using a PAT. #790
- full changelog is here: https://github.com/Kong/deck/blob/main/CHANGELOG.md

* Sat Nov 12 2022 Udo Seidel <udoseidel@gmx.de> 1.16.1-1
- first version release of SPEC

