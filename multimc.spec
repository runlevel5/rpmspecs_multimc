%global libnbtplusplus_commit 92f8d57227feb94643378ecf595626c60c0f59b8
%global quazip_commit 3691d57d3af13f49b2be2b62accddefee3c26b9c

Name:           multimc
Version:        0.6.7
Release:        2%{?dist}
Summary:        Minecraft launcher with ability to manage multiple instances

License:        Apache 2.0
URL:            https://multimc.org
Source0:        https://github.com/MultiMC/MultiMC5/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://github.com/MultiMC/libnbtplusplus/archive/%{libnbtplusplus_commit}.tar.gz
Source2:        https://github.com/MultiMC/quazip/archive/%{quazip_commit}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake3
BuildRequires:  zlib-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  java-1.8.0-openjdk-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  desktop-file-utils

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


%build
%cmake3 -DCMAKE_BUILD_TYPE=RelWithDebInfo \
        -DMultiMC_LAYOUT=lin-system \
        -DMultiMC_LIBRARY_DEST_DIR=%{_libdir}/%{name} \
        -DMultiMC_UPDATER=OFF \
        .

%make_build


%install
rm -rf $RPM_BUILD_ROOT
%make_install

# SVG Icon
install -d -m 0755 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -p -m 0644 application/resources/multimc/scalable/multimc.svg \
        %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

# Desktop file installation
desktop-file-install application/package/linux/multimc.desktop

# Fix libs
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
echo "%{_libdir}/%{name}" > "%{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf"


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


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
* Tue Sep 17 2019 ElXreno <elxreno@gmail.com> - 0.6.7-2
- Rebuild for F31

* Sun Aug 11 2019 ElXreno <elxreno@gmail.com> - 0.6.7
- Updated to 0.6.7 version

* Sat Jul 27 2019 ElXreno <elxreno@gmail.com> - 0.6.6
- Init packaging
