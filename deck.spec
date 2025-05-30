%define         pkgname         deck
%global         forgeurl        https://github.com/Kong/%{pkgname}
%global 	debug_package %{nil}
%global 	shortcommit 308526f
%define 	_build_id_links none

Name:		%{pkgname}
Version:        1.47.0
Release:	1%{?dist}
License:	Apache License v2.0
Vendor:		Kong Inc.
URL:		%{forgeurl}
Source0:	https://github.com/Kong/%{pkgname}/releases/download/v%{version}/v%{version}.tar.gz
Summary: 	Declarative configuration for Kong

BuildRequires:  golang >= 1.22.4  git

%description 
Declarative configuration for Kong

%prep
%autosetup

%setup

%build
export GOPROXY='https://proxy.golang.org,direct'
go build -o deck -ldflags "-s -w -X github.com/kong/deck/cmd.VERSION=%{version} -X github.com/kong/deck/cmd.COMMIT=%{shortcommit}"

%install
install -Dpm 0755 %{pkgname} %{buildroot}%{_bindir}/%{pkgname}

%files
%{_bindir}/deck

%changelog
* Sun May 11 2025 Udo Seidel <udoseidel@gmx.de> 1.47.0-1
- Added: Extended deck file convert command to be used for configuration migrations between LTS versions 2.8 and 3.4. The command can auto-fix the possible configurations and gives appropriate errors or warnings for the others. This is how it can be used: deck file convert --from 2.8 --to 3.4 --input-file kong-28x.yaml -o kong-34x.yaml #1610
- Added: _format_version string can be parametrised now and works well with deck file merge command as well as others. #1605 go-apiops #259

Fixed: ID existence checks are limited to certificates now, restoring sync performance. #1608 go-database-reconciler #254
Fixed: Bumped golang.org/x/net from 0.36.0 to 0.38.0 to account for CVE-2025-22872 #1601

* Sun Apr 13 2025 Udo Seidel <udoseidel@gmx.de> 1.46.3-1
- Bumping to the most recent version
- For changelog please go here: https://github.com/Kong/deck/blob/main/CHANGELOG.md

* Tue Feb 18 2024 Udo Seidel <udoseidel@gmx.de> 1.44.2-1
- Fix: Updated golang to version v1.23.5 to account for vulnerability CVE-2022-28948 #1497 #1533 

* Tue Feb 18 2024 Udo Seidel <udoseidel@gmx.de> 1.44.1-1
- Fix: Fixed issue coming with using deck against open-source Kong gateways where operations were getting stuck due to custom-entities support. Custom Entities are now gated to Enterprise gateways only. go-database-reconciler #1525

* Tue Feb 18 2024 Udo Seidel <udoseidel@gmx.de> 1.44.0-1
- Added support for consumer-group policy overrides in Kong Gateway version 3.4+ (until next major version is released). This is enabled via flag --consumer-group-policy-overrides in sync, diff and dump commands. Consumer-group policy overrides, though supported, are a deprecated feature in the Kong Gateway and users should consider moving to Consumer-group scoped plugins instead. Mixing of the two approaches should be avoided. #1518 go-database-reconciler #191
- Added support for managing degraphql_routes via deck for both Kong Gateway and Konnect. #1505 go-database-reconciler #154

* Fri Feb 07 2024 Udo Seidel <udoseidel@gmx.de> 1.43.1-1
- The deck gateway apply command added in v1.43.0 added additional HTTP calls to discover which functions are enabled. This does not work well when using an RBAC user with restricted permissions. This change removes those additional checks and delegates the lookup of foreign keys for partial applications to go-database-reconciler. #1508 go-database-reconciler #182

* Fri Feb 07 2024 Udo Seidel <udoseidel@gmx.de> 1.43.0-1
- Added deck gateway apply command that allows users to apply partial configuration to a running Gateway instance. #1459 go-database-reconciler #143
- Added support for private link global api endpoint for Konnect. #1500 go-database-reconciler #165
- Added flag --skip-consumers-with-consumer-groups for deck gateway dump command. If set to true, deck skips listing consumers with consumer-groups, thus gaining some performance with large configs. It is not valid for Konnect. #1486
- Adjusted multiline string formatting in terraform resource generation. #1482
- Improved error messaging when mandatory flag is missing in deck file convert. #1487
- Fixed deck gateway dump command that was missing associations between consumer-groups and consumers. #1486 go-database-reconciler #159 go-kong #494
- Added checks for all conflicting nested configs in plugins. A foreign key nested under a plugin of a different scope would error out. This would make sure that a sync does not go through when wrong configurations are passed via deck. go-database-reconciler #157
- Fixed req-validator config generation while using deck file openapi2kong command when both body and param schema are empty. #1501 go-apiops #244
- Fixed tags retention on entities while using select-tags. #1500 go-database-reconciler #156

* Thu Dec 26 2024 Udo Seidel <udoseidel@gmx.de> 1.42.1-1
- Fix: Updated golang.org/x/net to version v0.33.0 to account for vulnerability CVE-2024-45338 #1481 

* Fri Dec 13 2024 Udo Seidel <udoseidel@gmx.de> 1.42.0-1
- Add: new flag --online-entities-list to validate the specified entities via deck gateway validate command. #1458
- Add: feature to ignore entities tagged with konnect-managed during deck dump, sync and diff. This is valid for Konnect entities only. #1478 go-database-reconciler #153
- Add: Improved speed for deck sync/diff operations involving consumer-groups for gw 3.9+. The underlying API call to GET /consumer_group is called with query parameter list_consumers=false, making it faster for deck to deal with cases where a consumer-group holds many consumers. (#1475)[#1475] (go-kong #487)[Kong/go-kong#487] 
- Fix: issue where tags were not getting propagated to consumer-group plugins. #1478 go-database-reconciler #151 go-kong #485
- Fix: Enhanced help message for generate-imports-for-control-plane-id flag #1448
- Fix: Restored to using Gateway API generation in deck file kong2kic, rather than Ingress API #1431

* Fri Nov 29 2024 Udo Seidel <udoseidel@gmx.de> 1.41.4-1
- Add:  validation for ensuring that cookie parameters in parameter schemas are skipped and a warning is logged for the user while using deck file openapi2kong command. #1452 go-apiops #255
- Fix: issue where creating arrays with mixed types using oneOf in OAS specifications were failing while using deck file openapi2kong command. #1452 go-apiops #231

* Thu Nov 28 2024 Udo Seidel <udoseidel@gmx.de> 1.41.3-1
- Fix: Updated Konnect authentication logic to properly handle geo rewrites. #1451 go-database-reconciler #146
- Fix: false diffs for gateway by clearing unmatching deprecated fields from plugin schemas. #1451 go-database-reconciler #145 go-kong #473

* Sat Nov 09 2024 Udo Seidel <udoseidel@gmx.de> 1.41.2-1
- Fix: to validate for top-level type in parameter schemas in request-validator plugin while using deck file openapi2kong. go-apiops #215
- Add support for defining path parameters outside REST methods for request-validation while using deck file openapi2kong. go-apiops #216 (#1429)[#1429]

* Mon Oct 28 2024 Udo Seidel <udoseidel@gmx.de> 1.41.1-1
- Fix: deck gateway validate for Konnect supports Konnect configs passed by CLI flags now. Earlier, the validation was failing if control plane information was passed via CLI flags.

* Mon Oct 28 2024 Udo Seidel <udoseidel@gmx.de> 1.41.0-1
- Add deck gateway validate command now supports Konnect. Konnect entities can be validated online with this change. #1335
- Fix: Quoted type constraints are removed for Terraform. Type constraints in quotes were required in Terraform <= 0.11, It is now deprecated and will be removed in a future Terraform versions. Thus, removed them from kong2tf generation, so as to avoid potential errors in terraform apply. #1412

* Sun Sep 29 2024 Udo Seidel <udoseidel@gmx.de> 1.40.3-1
- Fix: the behaviour of --konnect-addr flag in case default Konnect URL is used with it. Earlier, using the default URL with the said flag ran the command against the gateway. #1398
- Bumped up go-apiops to v0.1.38 and replaced yaml/v3 package with Kong's own fork. This change allows deck commands to process OAS files with path lengths > 128 characters which was a limitation from the original yaml library.#1405 go-apiops #208 Kong/yaml #1

* Thu Sep 19 2024 Udo Seidel <udoseidel@gmx.de> 1.40.2-1
- Add support for default lookup services by @AntoineJac in #1367

* Sun Sep 15 2024 Udo Seidel <udoseidel@gmx.de> 1.40.1-1
- Fix: issue in deck file kong2tf command where users were facing a panic error with using jwt plugins when passing an empty list to cookie_names field. #1399
- Fix: Bumped up go-apiops library. The updated lib has a fix for deck file openapi2kong command where parameters.required field was coming as null, if not passed by user. #1400 go-apiops #205
- Fix: Bumped up go-kong library. The updated lib prevents unset plugin's configuration "record" fields to be filled with empty tables: {} for deck files. Since, deck doesn't fill defaults anymore, this fix ensures that deck doesn't pass empty record fields while syncing plugin configurations. #1401 go-kong #467

* Sun Sep 15 2024 Udo Seidel <udoseidel@gmx.de> 1.40.0-1
- Added a new file kong2tf command to convert a deck file to Terraform configuration #1391, along with two command line flags:
	--generate-imports-for-control-plane-id: If this is provided, import blocks will be added to Terraform to adopt existing resources.
	--ignore-credential-changes: If this is provided, any credentials will be ignored until they are destroyed and recreated.
- Fix: issue that was preventing a consumer to be in more than one consumer-groups #1394 go-database-reconciler #140
- Fix: Fields marked as auto in schema are filled with nil in the config sent to the Control Plane. In case a field is marked as auto and is a required field, deck would throw an error if the user doesn't fill it in the declarative configuration file. #1394 go-database-reconciler #139
- Fix: Defaults are no longer filled by deck. They will only be used for computing a diff, but not sent to the Control Plane. #1394 go-database-reconciler #133

* Wed Sep 04 2024 Udo Seidel <udoseidel@gmx.de> 1.39.6-1
- Fix: issue where plugins scoped to consumer-groups were shown as global by deck. #1380 go-database-reconciler #134

* Sun Aug 25 2024 Udo Seidel <udoseidel@gmx.de> 1.39.5-1
- Fix: deck file openapi2kong command where parameter schema wasn't getting generated properly. #1355 go-apiops #186 

* Thu Aug 01 2024 Udo Seidel <udoseidel@gmx.de> 1.39.4-1
- Fix: Correct --no-color flag behaviour in non-tty environments The changes retain the default behaviour of showing colors in tty and no colors in non-tty if no flag is passed. However, on passing the --no-color=false, non-tty environments can also get colored output.#1339
- Fix: Add validation on deck file patch to avoid confusing behaviour. The command intends to patch input files either via selector-value flags or command arguments. The change ensures that at least one of these is present, but not both at the same time.#1342
- Fix: rendering for expression routes, keeping kong gateway version in consideration. go-database-reconciler #118 #1351

* Tue Jul 16 2024 Udo Seidel <udoseidel@gmx.de> 1.39.3-1
- Fix: #1228 by updating the golang version from 1.21 to 1.22, thus removing the inconsistency between decK releases' version and the one used in the project. #1336 

* Thu Jul 04 2024 Udo Seidel <udoseidel@gmx.de> 1.39.2-1
- Fix: correct IPv6 targets comparison to avoid misleading diffs and failing syncs. #1333 go-database-reconciler #109
- Fix: make lookups for consumer-group's consumers more performant. #1333 go-database-reconciler #102

* Mon Jul 01 2024 Udo Seidel <udoseidel@gmx.de> 1.39.1-1
- Bumped CodeGen #1319

* Sat Jun 29 2024 Udo Seidel <udoseidel@gmx.de> 1.39.0-2
- Update BUILD requirements
- Fixed bogus date in SPEC changelog

* Fri Jun 28 2024 Udo Seidel <udoseidel@gmx.de> 1.39.0-1
- Fix: Bump Go version to 1.22.4 #1321

* Wed May 29 2024 Udo Seidel <udoseidel@gmx.de> 1.38.1-1
- Fix: Correct bug on plugins config comparison. #1311 go-database-reconciler #95

* Mon May 27 2024 Udo Seidel <udoseidel@gmx.de> 1.38.0-1
- Added openapi2kong now generates request-validator schemas for content-types with +json suffix. #1303 go-apiops #175
- Fix: Correct plugins config comparison to avoid misleading diffs. #1306 go-database-reconciler #93
- Fix: Make KIC v2 Gateway API v2 config generation deterministic. #1302
- Fix: Correct tags filtering with Consumers and Consumer Groups. #1293 go-database-reconciler #88
- Fix: Correct tags filtering with Consumers and Consumer Groups. #1293 go-database-reconciler #88
- Fix: Correct typo in inso-compatible flag of openapi2kong command. #1295
- Fix: Correct bad example on the add-plugins command cli help. #1294
- Fix: Removed the unsupported json-output flag from validate #1278
- Fix: Fixed race condition in lint command (bump vacuum library) #1281

* Wed Apr 10 2024 Udo Seidel <udoseidel@gmx.de> 1.37.0-1
- Added a --konnect-compatibility flag to deck gateway validate that validates Konnect readiness from an existing decK state. #1227

* Wed Apr 10 2024 Udo Seidel <udoseidel@gmx.de> 1.36.2-1
- Fix: Auto-generate rla (rate-limiting-advanced) namespaces in the convert subcommand when using Consumer Groups too. #1263
- Fix: OpenAPI 2 Kong: change regex priority field to int from uint, to allow for negative priorities. go-apiops # 162

* Thu Mar 21 2024 Udo Seidel <udoseidel@gmx.de> 1.36.1-1
- Fix: Avoid showing bogus diffs due to endpoint_permission roles array not being sorted. #71 go-database-reconciler
- Fix: Do not fetch Kong version when using validate command. #1247

* Thu Mar 14 2024 Udo Seidel <udoseidel@gmx.de> 1.36.0-1
- Added: This completes the namespace feature, by adding the host-based namespacing to the existing path-based namespacing. #1241
- Fix: Use correct workspace when running online validation. #1243
- Fix: Limit path-param names to 32 chars (go-apiops) #153 go-apiops
- Fix: Correct various issues with the file kong2kic command. #1230


* Mon Mar 04 2024 Udo Seidel <udoseidel@gmx.de> 1.35.1-1
- added GOPROXY settings to make the build work on Fedora (https://github.com/golang/go/issues/36624#issuecomment-575612165)

* Thu Feb 29 2024 Udo Seidel <udoseidel@gmx.de> 1.35.0-1
- Added a new file kong2kic command to convert a Kong declarative file to k8s resources for the Kong Ingress Controller (supports Ingress and Gateway resources). #1050
- Fix: auto-generate rla (rate-limiting-advanced) namespaces in the convert subcommand. #1206

* Thu Feb 08 2024 Udo Seidel <udoseidel@gmx.de> 1.34.0-1
- Fix: Correct consumer_groups -> consumers reference and allow importing their relationships from upstream using default_lookup_tags. #1212 go-database-reconciler #57
- Fix: CLI fix: error out if deck file addplugins gets a --selector but no --config. #1211

* Thu Feb 01 2024 Udo Seidel <udoseidel@gmx.de> 1.33.0-1
- Fix: Correct a defect preventing TLS configuration flags from being used with Konnect. #1194 go-database-reconciler #52

* Mon Jan 29 2024 Udo Seidel <udoseidel@gmx.de> 1.32.1-1
- Fix: Correct a defect preventing the use of plugins config deduplication when consumer-group scoped plugins are used. #1190 go-database-reconciler #45

* Thu Jan 25 2024 Udo Seidel <udoseidel@gmx.de> 1.32.0-1
- Added a new file namespace command to facilitate path-based namespacing. #1179 

* Mon Jan 22 2024 Udo Seidel <udoseidel@gmx.de> 1.31.1-1
- Fix: bug when using consumer-group scoped plugins with multiple nested entities. #1177 go-database-reconciler #45

* Mon Jan 22 2024 Udo Seidel <udoseidel@gmx.de> 1.31.0-1
- Fix: Added missing analytics for file commands. #1171
- Added support to default_lookup_tags to pull entities not part of the configuration file. #1124 #1173

* Mon Jan 15 2024 Udo Seidel <udoseidel@gmx.de> 1.30.0-1
- Fix: Correct bug when consumer-group-consumer doesn't have an username. #1113
- Fix: Improve deprecation warnings to reduce upgrade friction and show warning when reading STDIN from terminal. #1115
- Fix: 'file openapi2kong': Server ports will now be properly parsed, 32767 to 65535 are now accepted. apiops #105
- Added 'file openapi2kong': will now generate OpenIDConnect plugins. apiops #107
- Refactored: Moved the database reconciler to its own project. #1109

* Wed Nov 08 2023 Udo Seidel <udoseidel@gmx.de> 1.29.2-1
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

