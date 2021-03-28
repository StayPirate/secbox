#
# spec file for package secbox
#
# Copyright (c) 2020 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

%define archive_prefix secbox
%define secboxdir %{_prefix}/bin

Name:           secbox
Version:        1.0
Release:        0
Summary:        Toolbox that provides an out-of-the-box working setup
License:        MIT
Group:          Development/Tools/Other
URL:            https://github.com/StayPirate/secbox
Source:         %{archive_prefix}-%{version}.tar.xz
BuildArch:      noarch
Requires:       podman
Requires:       curl

%description
Secbox is a toolbox that provides an out-of-the-box working setup for your
daily work in the SUSE Security Team.

It does not only manage the toolset but it also takes care of mounting the
required NFS exports. Think at this as a portable workstation setup. It makes
hard use of Podman as container engine, so make sure it's installed on your
machine and configured to run rootless. Your home directory will be mounted
as home directory within the container, this makes all your dotfiles accessible
from the preinstalled tools. The first time you run this script the container
will be created. The best way to use this script from your terminal is by
leveraging aliases. Use 'secbox --alias' to get a list of suggested ones.

This tool is only intended for people with access to the SUSE internal
network.

%prep
%setup -q -n %{archive_prefix}-%{version}

%build

%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 secbox %{buildroot}%{_bindir}

%files
%{_bindir}/secbox

%changelog
