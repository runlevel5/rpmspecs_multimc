# Enable Ninja build
%bcond_without ninja_build

%global libnbtplusplus_commit       dc72a20b7efd304d12af2025223fad07b4b78464
%global libnbtplusplus_shortcommit  %(c=%{libnbtplusplus_commit}; echo ${c:0:7})
%global quazip_commit               b1a72ac0bb5a732bf887a535ab75c6f9bedb6b6b
%global quazip_shortcommit          %(c=%{quazip_commit}; echo ${c:0:7})

Name:           multimc
Version:        0.6.16
Release:        1%{?dist}
Summary:        Minecraft launcher with ability to manage multiple instances

#
# CC-BY-SA
# ---------------------------------------
# application/resources/multimc/
#
# BSD 3-clause "New" or "Revised" License
# ---------------------------------------
# application/
# libraries/LocalPeer/
# libraries/ganalytics/
#
# Boost Software License (v1.0)
# ---------------------------------------
# cmake/
#
# Expat License
# ---------------------------------------
# libraries/systeminfo/
#
# GNU Lesser General Public License (v2 or later)
# ---------------------------------------
# libraries/rainbow
#
# GNU Lesser General Public License (v2.1 or later)
# ---------------------------------------
# libraries/iconfix/
# libraries/quazip/
#
# GNU Lesser General Public License (v3 or later)
# ---------------------------------------
# libraries/libnbtplusplus/
#
# GPL (v2)
# ---------------------------------------
# libraries/pack200/
#
# ISC License
# ---------------------------------------
# libraries/hoedown/
#
# zlib/libpng license
# ---------------------------------------
# libraries/quazip/quazip/unzip.h
# libraries/quazip/quazip/zip.h
#

License:        CC-BY-SA and ASL 2.0 and BSD and Boost and LGPLv2 and LGPLv2+ and LGPLv3+ and GPLv2 and GPLv2+ and ISC and zlib
URL:            https://multimc.org
Source0:        https://github.com/MultiMC/Launcher/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/MultiMC/libnbtplusplus/archive/%{libnbtplusplus_commit}/libnbtplusplus-%{libnbtplusplus_shortcommit}.tar.gz
Source2:        https://github.com/MultiMC/quazip/archive/%{quazip_commit}/quazip-%{quazip_shortcommit}.tar.gz
Source3:        %{expand:%%(pwd)/multimc.svg}
Source4:        %{expand:%%(pwd)/multimc.desktop}
Source5:        %{expand:%%(pwd)/multimc.metainfo.xml}
Source6:        %{expand:%%(pwd)/runner.sh}

Patch1:         0001-fix-compilation-issue.patch
Patch2:         0002-add-lin-system-layout.patch
Patch3:         0003-add-msa-client-id.patch

%if %{with ninja_build}
BuildRequires:  ninja-build
%endif

BuildRequires:  cmake3
BuildRequires:  /usr/bin/appstream-util
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++

# Fix warning: Could not complete Guile gdb module initialization from:
# /usr/share/gdb/guile/gdb/boot.scm
BuildRequires:  gdb-headless

BuildRequires:  java-devel
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(zlib)

Requires:       hicolor-icon-theme
Requires:       java-headless

Recommends:     xrandr


%description
MultiMC is a free, open source launcher for Minecraft. It allows you to have
multiple, separate instances of Minecraft (each with their own mods, texture
packs, saves, etc) and helps you manage them and their associated options with
a simple interface.


%prep
%autosetup -p1 -n Launcher-%{version}

tar -xvf %{SOURCE1} -C libraries
tar -xvf %{SOURCE2} -C libraries
rmdir libraries/libnbtplusplus libraries/quazip
mv -f libraries/quazip-%{quazip_commit} libraries/quazip
mv -f libraries/libnbtplusplus-%{libnbtplusplus_commit} libraries/libnbtplusplus

cp %{SOURCE3} .
cp %{SOURCE4} .
cp %{SOURCE5} .
cp %{SOURCE6} .

%build
%cmake \
    %{?with_ninja_build: -GNinja} \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DLauncher_NOTIFICATION_URL:STRING=https://files.multimc.org/notifications.json \
    -DCMAKE_INSTALL_PREFIX=/opt/%{name} \
    -DLauncher_EMBED_SECRETS=OFF \
    -DLauncher_LAYOUT=lin-system \
    .

%cmake_build


%install
%cmake_install

# Install SVG icon...
install -Dp -m 0644 ./multimc.svg \
        %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

# Install desktop file...
desktop-file-install ./multimc.desktop

# Install metainfo XML file...
mkdir -p %{buildroot}%{_metainfodir}
install -m 0644 ./multimc.metainfo.xml %{buildroot}%{_metainfodir}/multimc.metainfo.xml

# Install the runner file...
mkdir -p %{buildroot}%{_bindir}
install -m 0755 ./runner.sh %{buildroot}%{_bindir}/%{name}

# Proper library linking...
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
echo "/opt/%{name}/lib" > "%{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf"

%check
%ctest %{?_smp_mflags}
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}/%{_metainfodir}/multimc.metainfo.xml

%files
%license COPYING.md
%doc README.md changelog.md
%{_bindir}/%{name}
/opt/%{name}/*
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/applications/%{name}.desktop
%{_metainfodir}/multimc.metainfo.xml
%config %{_sysconfdir}/ld.so.conf.d/*

%changelog
* Sat Sep 23 2023 Trung Lê <8@tle.id.au> - 0.6.16-1
- Update to version 0.6.16
- Restore the deleted lin-system LAYOUT in CMakeList.txt
- Bundle the metainfo, desktop and runner

* Fri Sep 24 2021 ElXreno - 0.6.13-1
- Update to version 0.6.13
  Add recommended dependency (@critbase request)

* Fri May 28 2021 ElXreno <elxreno@gmail.com> - 0.6.12-2
- Fix build on Fedora 34

* Mon Mar 22 2021 ElXreno <elxreno@gmail.com> - 0.6.12-1
- Update to version 0.6.12

* Wed Nov 11 11:37:26 +03 2020 ElXreno <elxreno@gmail.com> - 0.6.11-3
- Update libnbtplusplus to commit dc72a20

* Sun Apr 19 2020 ElXreno <elxreno@gmail.com> - 0.6.11-2
- Replaced java-1.8.0-openjdk by java-headless

* Mon Mar 30 2020 ElXreno <elxreno@gmail.com> - 0.6.11-1
- Updated to version 0.6.11

* Sat Mar 14 2020 ElXreno <elxreno@gmail.com> - 0.6.8-2
- Add java-11-openjdk as recommended package

* Sun Feb 09 2020 ElXreno <elxreno@gmail.com> - 0.6.8-1
- Updated to version 0.6.8

* Sat Jan 04 2020 ElXreno <elxreno@gmail.com> - 0.6.7-5
- Updated libnbtplusplus to commit 508eda831686c6d89b75bbb49d91e01b0f73d2ad
- Added check entry
- Added notification url
- Fixed license and added licenses breakdown

* Thu Nov 28 2019 ElXreno <elxreno@gmail.com> - 0.6.7-4
- Fixed license

* Wed Sep 18 2019 ElXreno <elxreno@gmail.com> - 0.6.7-3
- Rebuild for Rawhide

* Tue Sep 17 2019 ElXreno <elxreno@gmail.com> - 0.6.7-2
- Rebuild for F31

* Sun Aug 11 2019 ElXreno <elxreno@gmail.com> - 0.6.7
- Updated to 0.6.7 version

* Sat Jul 27 2019 ElXreno <elxreno@gmail.com> - 0.6.6
- Init packaging
