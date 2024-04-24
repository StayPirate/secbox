#
# spec file for package secbox
#
# Please submit bugfixes or comments via https://github.com/StayPirate/secbox
#

%define archive_prefix secbox

Name:           secbox
Version:        1.21
Release:        0
Summary:        Toolbox for your daily work at the SUSE Security Team
License:        MIT
Group:          Development/Tools/Other
URL:            https://github.com/StayPirate/secbox
Source:         %{archive_prefix}-%{version}.tar.xz
BuildArch:      noarch
Requires:       podman
Requires:       curl
Recommends:     openssh

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

%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 secbox %{buildroot}%{_bindir}

%files
%{_bindir}/secbox

%changelog
