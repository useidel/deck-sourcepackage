%define         pkgname         deck
%global         forgeurl        https://github.com/Kong/%{pkgname}
%global 	debug_package %{nil}
%define 	_build_id_links none

Name:		%{pkgname}
Version:        1.18.1
Release:	1%{?dist}
License:	Apache License v2.0
Vendor:		Kong Inc.
URL:		%{forgeurl}
Source0:	https://github.com/Kong/%{pkgname}/releases/download/v%{version}/v%{version}.tar.gz
Summary: 	Declarative configuration for Kong

BuildRequires:  golang git

%description 
Declarative configuration for Kong

%prep
%autosetup

%setup

%build
go build

%install
install -Dpm 0755 %{pkgname} %{buildroot}%{_bindir}/%{pkgname}

%files
%{_bindir}/deck

%changelog
* Sat Feb 11 2023 Udo Seidel <udoseidel@gmx.de> 1.18.1-1
- c7f142e fix: use global endpoint to retrieve Konnect org info

* Thu Feb 09 2023 Udo Seidel <udoseidel@gmx.de> 1.18.0-1
- Remove deprecated endpoint for pinging Konnect so to add Konnect System Accounts access token support. #843
- full changelog is here: https://github.com/Kong/deck/blob/main/CHANGELOG.md

* Tue Feb 07 2023 Udo Seidel <udoseidel@gmx.de> 1.17.3-1
- Handle konnect runtime groups pagination properly. #841
- Fix workspaces validation with multiple files #839
- full changelog is here: https://github.com/Kong/deck/blob/main/CHANGELOG.md

* Tue Jan 24 2023 Udo Seidel <udoseidel@gmx.de> 1.17.2-1
- Allow writing execution output to stdout in Konnect mode. #829
- Add tags support to Consumer Groups #823
- Add "update" functionality to Consumer Groups #823
- Do not error out when EE list endpoints are hit but no license is present in Kong Gateway. #821
- out of band patch removed
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

