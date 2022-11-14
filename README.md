# deck-sourcepackage

This repo maintains a RPM SPEC file for [Kong deck](https://github.com/Kong/deck) 
which is a declarative configuration of Kong. 
The project uses [goreleaser](https://goreleaser.com/) to produce RPMs and DEBs for 
the [releases](https://github.com/Kong/deck/releases/). 
But these are binary only and not so easy to subscribe to for automated 
updates via YUM/DNF/ZYPPER or APT.

With this RPM SPEC file and facilitating the build plattform [Copr](https://copr.fedorainfracloud.org/) 
I can easily create source and binary packages and make them accessible for YUM/DNF/ZYPPER.

I would like to cover that for DEB as well but this needs more research or a build plattform which 
provides the needed framework (offering Debian and allowing internet access during the build).

Additional information: There as a [discussion](https://github.com/goreleaser/goreleaser/issues/3136) which pointed to [go2rpm](https://pagure.io/GoSIG/go2rpm) and [dh-make-golang](https://go-team.pages.debian.net/), respectively. This might be another way to go.
