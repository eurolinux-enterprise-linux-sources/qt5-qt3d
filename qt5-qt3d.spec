%global qt_module qt3d

%define docs 1

#define prerelease

Summary: Qt5 - Qt3D QML bindings and C++ APIs
Name:    qt5-%{qt_module}
Version: 5.6.2
Release: 1%{?dist}

# See LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt, for details
# See also http://doc.qt.io/qt-5/licensing.html
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url:     http://www.qt.io
Source0: http://download.qt.io/official_releases/qt/5.6/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz

Patch0:  qt3d-fix-build-on-big-endian-architectures.patch

BuildRequires:  cmake
BuildRequires:  qt5-qtbase-static >= %{version}
BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  pkgconfig(Qt5XmlPatterns)
BuildRequires:  pkgconfig(Qt5Qml)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5XmlPatterns)
BuildRequires:  pkgconfig(Qt5OpenGL)

Requires:       qt5-qtimageformats%{?_isa} >= %{version}

%{?_qt5:Requires: %{_qt5}%{?_isa} >= %{_qt5_version}}

%description
Qt 3D provides functionality for near-realtime simulation systems with
support for 2D and 3D rendering in both Qt C++ and Qt Quick applications).

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%if 0%{?docs}
%package doc
Summary: API documentation for %{name}
License: GFDL
Requires: %{name} = %{version}-%{release}
BuildRequires: qt5-qdoc
BuildRequires: qt5-qhelpgenerator
BuildArch: noarch
%description doc
%{summary}.
%endif

%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}

%patch0 -p1 -b .fix-build-on-big-endian-architectures

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{qmake_qt5} ..

make %{?_smp_mflags}

%if 0%{?docs}
# HACK to avoid multilib conflicts in noarch content
# see also https://bugreports.qt-project.org/browse/QTBUG-42071
QT_HASH_SEED=0; export QT_HASH_SEED
make %{?_smp_mflags} docs
%endif
popd

%install
make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}

%if 0%{?docs}
make install_docs INSTALL_ROOT=%{buildroot} -C %{_target_platform}
%endif

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE.GPL* LICENSE.LGPL*
%{_qt5_libdir}/libQt53DQuick.so.5*
%{_qt5_libdir}/libQt53DInput.so.5*
%{_qt5_libdir}/libQt53DQuickRender.so.5*
%{_qt5_libdir}/libQt53DRender.so.5*
%{_qt5_libdir}/libQt53DCore.so.5*
%{_qt5_libdir}/libQt53DLogic.so.5*
%{_qt5_libdir}/libQt53DQuickInput.so.5*
%{_qt5_archdatadir}/qml/Qt3D/
%{_qt5_archdatadir}/qml/QtQuick/Scene3D
%{_qt5_plugindir}/sceneparsers/libassimpsceneparser.so
%{_qt5_plugindir}/sceneparsers/libgltfsceneparser.so

%files devel
%{_qt5_bindir}/qgltf
%{_qt5_libdir}/libQt53DQuick.so
%{_qt5_libdir}/libQt53DQuick.prl
%{_qt5_libdir}/cmake/Qt53DQuick
%{_qt5_headerdir}/Qt3DQuick
%{_qt5_libdir}/pkgconfig/Qt53DQuick.pc
%{_qt5_libdir}/libQt53DInput.so
%{_qt5_libdir}/libQt53DInput.prl
%{_qt5_libdir}/cmake/Qt53DInput
%{_qt5_headerdir}/Qt3DInput/
%{_qt5_libdir}/pkgconfig/Qt53DInput.pc
%{_qt5_libdir}/libQt53DCore.so
%{_qt5_libdir}/libQt53DCore.prl
%{_qt5_libdir}/cmake/Qt53DCore/
%{_qt5_headerdir}/Qt3DCore/
%{_qt5_libdir}/pkgconfig/Qt53DCore.pc
%{_qt5_libdir}/libQt53DQuickRender.so
%{_qt5_libdir}/libQt53DQuickRender.prl
%{_qt5_libdir}/cmake/Qt53DQuickRender/
%{_qt5_headerdir}/Qt3DQuickRender/
%{_qt5_libdir}/pkgconfig/Qt53DQuickRender.pc
%{_qt5_libdir}/libQt53DRender.so
%{_qt5_libdir}/libQt53DRender.prl
%{_qt5_libdir}/cmake/Qt53DRender/
%{_qt5_headerdir}/Qt3DRender/
%{_qt5_libdir}/pkgconfig/Qt53DRender.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri
%{_qt5_libdir}/libQt53DLogic.so
%{_qt5_libdir}/libQt53DLogic.prl
%{_qt5_headerdir}/Qt3DLogic/
%{_qt5_libdir}/cmake/Qt53DLogic
%{_qt5_libdir}/pkgconfig/Qt53DLogic.pc
%{_qt5_libdir}/libQt53DQuickInput.so
%{_qt5_libdir}/libQt53DQuickInput.prl
%{_qt5_headerdir}/Qt3DQuickInput/
%{_qt5_libdir}/cmake/Qt53DQuickInput
%{_qt5_libdir}/pkgconfig/Qt53DQuickInput.pc

%if 0%{?docs}
%files doc
%{_qt5_docdir}/*
%endif

%if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif


%changelog
* Wed Jan 11 2017 Jan Grulich <jgrulich@redhat.com> - 5.6.2-1
- Update to 5.6.2
  Resolves: bz#1384836

* Tue Aug 30 2016 Jan Grulich <jgrulich@redhat.com> - 5.6.1-10
- Increase build version to have newer version than in EPEL
  Resolves: bz#1324732

* Wed Jun 08 2016 Jan Grulich <jgrulich@redhat.com> - 5.6.1-1
- Update to 5.6.1
  Resolves: bz#1324732

* Thu Apr 07 2016 Jan Grulich <jgrulich@redhat.com> - 5.6.0-3
- Initial version for RHEL
  Resolves: bz#1324732

* Tue Mar 22 2016 Rex Dieter <rdieter@fedoraproject.org>  - 5.6.0-2
- rebuild

* Mon Mar 14 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-1
- 5.6.0 final release

* Tue Feb 23 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.9.rc
- Update to final RC

* Mon Feb 15 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.8
- Update RC release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-0.7.beta
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 28 2015 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.6.beta
- use %%license, update Source URL, BR: cmake

* Mon Dec 21 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.5
- Update to final beta release

* Fri Dec 11 2015 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.4
- -doc: BR: qt5-qdoc qt5-qhelpgenerator

* Thu Dec 10 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.3
- Official beta release

* Thu Dec 10 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.2
- Official beta release

* Tue Nov 03 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.1
- Start to implement 5.6.0 beta

* Tue Nov 03 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.1
- Start to implement 5.6.0 beta

* Thu Oct 15 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.1-2
- Update to final release 5.5.1

* Tue Sep 29 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.1-1
- Update to Qt 5.5.1 RC1

* Wed Jul 1 2015 Helio Chissini de Castro <helio@kde.org> 5.5.0-1
- New final upstream release Qt 5.5.0

* Thu Jun 25 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.2.rc
- Update for official RC1 released packages

* Wed Jun 17 2015 Daniel Vrátil <dvratil@redhat.com> - 5.5.0-0.1.rc
- Qt 5.5.0 RC1 (initial version)

