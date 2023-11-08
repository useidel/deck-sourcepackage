%define         pkgname         deck
%global         forgeurl        https://github.com/Kong/%{pkgname}
%global 	debug_package %{nil}
%global 	shortcommit 77682ca
%define 	_build_id_links none

Name:		%{pkgname}
Version:        1.29.2
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
go build -o deck -ldflags "-s -w -X github.com/kong/deck/cmd.VERSION=%{version} -X github.com/kong/deck/cmd.COMMIT=%{shortcommit}"

%install
install -Dpm 0755 %{pkgname} %{buildroot}%{_bindir}/%{pkgname}

%files
%{_bindir}/deck

%changelog
* Wed Nov 0 2023 Udo Seidel <udoseidel@gmx.de> 1.29.2-1
- Fix: Avoid unnecessary Konnect API call to retrieve its version. #1095
- Fix: Correct default values when using gateway dump. #1094

* Tue Nov 07 2023 Udo Seidel <udoseidel@gmx.de> 1.29.1-1
- Fix: Correct a bug preventing logins with Konnect in the EU region. #1089

* Fri Nov 03 2023 Udo Seidel <udoseidel@gmx.de> 1.29.0-1
- Added support for konnect AU region. #1082
- Fix: Resolved an issue in the deck file validate and deck gateway validate commands that prevented them from properly processing the provided file arguments. #1084

* Thu Nov 02 2023 Udo Seidel <udoseidel@gmx.de> 1.28.1-1
- Old cli commands would also output to stdout by default. Now back to default "kong.yaml". #1073
- Deprecation warnings were send to stdout, mixing warnings with intended output. Now going to stderr. #1075

* Tue Oct 31 2023 Udo Seidel <udoseidel@gmx.de> 1.28.0-1
- Added Allow arrays to be specified on the file patch CLI command. #1056
- Fix: Do not overwrite created_at for existing resources when running sync command. #1061
- Fix: deck file openapi2kong creates names for entities that differ from the older inso tool. This has been fixed, but requires the new --inso-compatible flag to not be breaking. Adding that flag will also skip id generation. #962 
- Changed Add analytics for local operations #1051
- Changed The top-level CLI commands have been restructured. All commands now live under 2 subcommands (gateway and file) to clarify their use and (in the future) reduce the clutter of the many global flags only relevant to a few commands. The new commands are more unix-like, and preferably default to stdin/stdout and no longer to "kong.yaml". Using the old commands will still work but will print a deprecation notice. Please update your usage to the new commands. #962

* Thu Sep 28 2023 Udo Seidel <udoseidel@gmx.de> 1.27.1-1
- Fix: inconsistency when managing multiple consumers having equal username and custom_id fields. #1037
- Fix: Correct a bug preventing the deprecated --konnect-runtime-group-name flag to work properly. #1036

* Tue Sep 26 2023 Udo Seidel <udoseidel@gmx.de> 1.27.0-1
- Added --konnect-control-plane-name flag and deprecate --konnect-runtime-group-name #1000
- Fix: Bumped go-apiops to v0.1.21 to include various fixes on APIOps functionality #1029

* Thu Sep 07 2023 Udo Seidel <udoseidel@gmx.de> 1.26.1-1
- Fix: raise error if files have different Runtime Groups
- Fix: correct consumers validation when custom_id is used #1012 
- Fix: change go-apiops in examples to deck file
- Fix: remove errant comma from CLI example
- Fix: set default strip_path to true

* Wed Aug 09 2023 Udo Seidel <udoseidel@gmx.de> 1.26.0-1
- Added support for scoping plugins to Consumer Groups for both Kong Gateway and Konnect. #963 #959
- Fix: Remove fallback mechanism formely used to authenticate with either "old" or "new" Konnect. #995

* Sat Jul 29 2023 Udo Seidel <udoseidel@gmx.de> 1.25.0-1
- Added a new command file render to render a final decK file. This will result in a file representing the state as it would be synced online. #963
- Added a new flag --format to file convert to enable JSON output. #963
- Use same interface to pull Consumer Groups with Kong Gateway and Konnect. This will help solving the issue of using tags with Consumer Groups when running against Konnect. #984
- Fix Consumers handling when a consumer's custom_id is equal to the username of another consumer. #986
- Avoid misleading diffs when configuration file has empty tags. #985

* Mon Jul 24 2023 Udo Seidel <udoseidel@gmx.de> 1.24.0-2
- fixed wrong date format in changelog of SPEC file

* Mon Jul 24 2023 Udo Seidel <udoseidel@gmx.de> 1.24.0-1
- Add a new flag (--json-output) to enable JSON output when using sync and diff commands #798 
- Improved error logs coming from files validation against Kong's schemas. #976
- Added a new command file openapi2kong that will generate a deck file from an OpenAPI 3.0 spec. This is the replacement for the similar inso functionality. The functionality is imported from the go-apiops library. #939
- Added a new command file merge that will merge multiple deck files. The files will not be validated, which allows for working with incomplete or even invalid files in a pipeline. The functionality is imported from the go-apiops library. #939
- Added a new command file patch for applying patches on top of a decK file. The patches can be provided on the commandline, or via patch files. The deck file will not be validated, which allows for working with incomplete or even invalid files in a pipeline. The functionality is imported from the go-apiops library. #939
- Added a new commands file add-tags/list-tags/remove-tags to manage tags in a decK file. The deck file will not be validated, which allows for working with incomplete or even invalid files in a pipeline. The functionality is imported from the go-apiops library. #939
- Added a new command file add-plugins for adding plugins to a decK file. The plugins can be provided on the commandline, or via config files. The deck file will not be validated, which allows for working with incomplete or even invalid files in a pipeline. The functionality is imported from the go-apiops library. #939
- Fix Certificates & SNIs handling when running against Konnect. #978

* Mon Jul 03 2023 Udo Seidel <udoseidel@gmx.de> 1.23.0-1
- Add Honor HTTPS_PROXY and HTTP_PROXY proxy environment variables #952

* Thu Jun 22 2023 Udo Seidel <udoseidel@gmx.de> 1.22.1-1
- Fix Handle missing service and route names detecting duplicates #945
- Fix Update go-kong to fix a bug causing a panic when filling record defaults of an empty array. #345

* Thu Jun 08 2023 Udo Seidel <udoseidel@gmx.de> 1.22.0-1
- Add indent function to support multi-line content #929 
- Fix Update go-kong to fix a bug causing wrong injection of defaults for non-required fields and set of record. go-kong #333 go-kong #336 

* Wed May 31 2023 Udo Seidel <udoseidel@gmx.de> 1.21.0-1
- Add support for updating Services, Routes, and Consumers by changing their IDs, but retaining their names. #918
- Fix Return proper error when HTTP calls fail on validate. #869
- Fix Replace old docs link in convert and fix its docstring. #905
- Misc Bump Go toolchain to 1.20. #898

* Mon Mar 27 2023 Udo Seidel <udoseidel@gmx.de> 1.19.1-2
- Added compile flags for version/tag and (short-)commit

* Mon Mar 27 2023 Udo Seidel <udoseidel@gmx.de> 1.19.1-1
- Add support to numeric environment variables injection via the toInt and toFloat functions. #868
- Add support to bolean environment variables injection via the toBool function. #867
- Skip Consumer Groups and the related plugins when --skip-consumers #863
- full changelog is here: https://github.com/Kong/deck/blob/main/CHANGELOG.md

* Tue Feb 21 2023 Udo Seidel <udoseidel@gmx.de> 1.19.0-1
- feat: add instance_name field to plugin schema
- full changelog is here: https://github.com/Kong/deck/blob/main/CHANGELOG.md

* Sat Feb 11 2023 Udo Seidel <udoseidel@gmx.de> 1.18.1-1
- c7f142e fix: use global endpoint to retrieve Konnect org info
- full changelog is here: https://github.com/Kong/deck/blob/main/CHANGELOG.md

* Thu Feb 09 2023 Udo Seidel <udoseidel@gmx.de> 1.18.0-1
- Remove deprecated endpoint for pinging Konnect so to add Konnect System Accounts access token support. #843
- abfull changelog is here: https://github.com/Kong/deck/blob/main/CHANGELOG.md

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

