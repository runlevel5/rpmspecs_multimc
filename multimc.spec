# Enable Ninja build
%bcond_without ninja_build

%global libnbtplusplus_commit 508eda831686c6d89b75bbb49d91e01b0f73d2ad
%global quazip_commit 3691d57d3af13f49b2be2b62accddefee3c26b9c

Name:           multimc
Version:        0.6.8
Release:        2%{?dist}
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
Source0:        https://github.com/MultiMC/MultiMC5/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/MultiMC/libnbtplusplus/archive/%{libnbtplusplus_commit}/libnbtplusplus-%{libnbtplusplus_commit}.tar.gz
Source2:        https://github.com/MultiMC/quazip/archive/%{quazip_commit}/quazip-%{quazip_commit}.tar.gz

%if %{with ninja_build}
BuildRequires:  ninja-build
%endif

BuildRequires:  cmake3
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++

# Fix warning: Could not complete Guile gdb module initialization from:
# /usr/share/gdb/guile/gdb/boot.scm
BuildRequires:  gdb-headless

BuildRequires:  java-1.8.0-openjdk-devel
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(zlib)

Requires:       hicolor-icon-theme
Requires:       java-1.8.0-openjdk

# Recommend java 11 for newest Minecraft versions
Recommends:     java-11-openjdk


%description
MultiMC is a free, open source launcher for Minecraft. It allows you to have
multiple, separate instances of Minecraft (each with their own mods, texture
packs, saves, etc) and helps you manage them and their associated options with
a simple interface.


%prep
%autosetup -n MultiMC5-%{version}

tar -xvf %{SOURCE1} -C libraries
tar -xvf %{SOURCE2} -C libraries
rmdir libraries/libnbtplusplus libraries/quazip
mv -f libraries/quazip-%{quazip_commit} libraries/quazip
mv -f libraries/libnbtplusplus-%{libnbtplusplus_commit} libraries/libnbtplusplus

mkdir -p %{_target_platform}


%build
pushd %{_target_platform}
%cmake \
    %{?with_ninja_build: -GNinja} \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DMultiMC_NOTIFICATION_URL:STRING=https://files.multimc.org/notifications.json \
    -DMultiMC_LAYOUT=lin-system \
    -DMultiMC_LIBRARY_DEST_DIR=%{_libdir}/%{name} \
    -DMultiMC_UPDATER=OFF \
    ..
popd

%if %{with ninja_build}
%ninja_build -C %{_target_platform}
%else
%make_build -C %{_target_platform}
%endif


%install
%if %{with ninja_build}
%ninja_install -C %{_target_platform}
%else
%make_install -C %{_target_platform}
%endif

# Install SVG icon...
install -d -m 0755 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -p -m 0644 application/resources/multimc/scalable/multimc.svg \
        %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

# Install desktop file...
desktop-file-install application/package/linux/multimc.desktop

# Proper library linking...
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
echo "%{_libdir}/%{name}" > "%{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf"


%check
%if %{with ninja_build}
%ninja_build test -C %{_target_platform}
%else
%make_build test -C %{_target_platform}
%endif
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license COPYING.md
%doc README.md changelog.md
%{_bindir}/%{name}
%{_libdir}/%{name}/*
%{_datadir}/%{name}/*
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/applications/%{name}.desktop
%config %{_sysconfdir}/ld.so.conf.d/*



%changelog
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
