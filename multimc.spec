%global libnbtplusplus_commit 508eda831686c6d89b75bbb49d91e01b0f73d2ad
%global quazip_commit 3691d57d3af13f49b2be2b62accddefee3c26b9c

Name:           multimc
Version:        0.6.7
Release:        4%{?dist}
Summary:        Minecraft launcher with ability to manage multiple instances

License:        ASL 2.0
URL:            https://multimc.org
Source0:        https://github.com/MultiMC/MultiMC5/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://github.com/MultiMC/libnbtplusplus/archive/%{libnbtplusplus_commit}.tar.gz
Source2:        https://github.com/MultiMC/quazip/archive/%{quazip_commit}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake3
BuildRequires:  desktop-file-utils

BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(gl)
BuildRequires:  java-1.8.0-openjdk-devel

Requires:       hicolor-icon-theme
Requires:       java-headless


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
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DMultiMC_LAYOUT=lin-system \
    -DMultiMC_LIBRARY_DEST_DIR=%{_libdir}/%{name} \
    -DMultiMC_UPDATER=OFF \
    ..
popd

%make_build -C %{_target_platform}


%install
%make_install -C %{_target_platform}

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
%make_build test -C %{_target_platform}
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
