%define wrappers_ver 1.0.3
%define oname ROX-Filer

Name:		rox
Version:	2.10
Release:	3
Summary:	A fast and powerful graphical file manager
Group:		Graphical desktop/Other
License:	GPL
URL:		https://rox.sourceforge.net
Source:		http://prdownloads.sourceforge.net/%{name}/%{name}-filer-%{version}.tar.bz2
Source1:	http://prdownloads.sourceforge.net/%{name}/Wrappers-%{wrappers_ver}.tar.bz2
Source2:	rox-48.png
Source3:	rox-32.png
Source4:	rox-16.png
Patch0:		rox-filer-2.10-linkage.patch
Patch1:		rox-filer-2.7-shell.patch
Patch2:		rox-2.1.0-gnuclient.patch
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(gnome-vfs-2.0)
BuildRequires:	pkgconfig(xt)
BuildRequires:	shared-mime-info

%description
ROX-Filer is a fast, powerful, and easy to use graphical file
manager. It has full support for drag-and-drop and application
directories.  The filer can also provide a pinboard (allowing you to pin
up files on your desktop background) and panels.  The emphasis is on
uncluttered directory views; menus and prompts only appear when needed.

The Wrappers package found on the Rox home page is already included.

%prep
%setup -q -a 1 -n rox-filer-%{version}
%patch0 -p1 -b .linkage
%patch1 -p1 -b .shell
%patch2 -p1 -b .gnuclient

%build
%setup_compile_flags
mkdir %{oname}/build
pushd %{oname}/build
../src/configure
%make
popd

%install
mkdir -p %{buildroot}%{_libdir}/apps
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_datadir}/mime/packages
cp -a %{oname} %{buildroot}%{_libdir}/apps/
rm -rf %{buildroot}%{_libdir}/apps/src
rm -rf %{buildroot}%{_libdir}/apps/*/{src,build}
cp -a rox.1 %{buildroot}%{_mandir}/man1
( cd %{buildroot}%{_mandir}/man1 ; ln -s rox.1 %{oname}.1 )
cat << EOF > %{buildroot}%{_bindir}/rox
#!/bin/sh
exec %{_libdir}/apps/%{oname}/AppRun "\$@"
EOF
chmod a+x %{buildroot}%{_bindir}/rox
cp rox.xml %{buildroot}%{_datadir}/mime/packages
cp -r Choices %{buildroot}%{_datadir}

# Wrappers
cp -a Wrappers/* %{buildroot}%{_libdir}/apps/
cp -a Wrappers/README README.wrappers

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=ROX
Comment=File Manager of the ROX desktop environment
Exec=%{_bindir}/%{name} %U
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-System-FileTools;System;FileManager;
EOF


install -D %{SOURCE2} %{buildroot}%{_liconsdir}/%{name}.png
install -D %{SOURCE3} %{buildroot}%{_iconsdir}/%{name}.png
install -D %{SOURCE4} %{buildroot}%{_miconsdir}/%{name}.png

# remove temp file
rm -f %{buildroot}%{_libdir}/apps/Netscape/.AppRun.swp %{buildroot}%{_datadir}/Choices/MIME-types/* %{buildroot}%{_libdir}/apps/ROX-Filer/AppRun.*

for langdir in %{buildroot}%{_libdir}/apps/%{oname}/Messages/*/;do
echo "%lang($(basename $langdir)) $(echo $langdir |sed s!%{buildroot}!!)" >> %{name}.lang
done

%files -f %{name}.lang
%doc README*
%doc %{_libdir}/apps/%{oname}/Help
%doc %{_libdir}/apps/%{oname}/Messages/README
%dir %{_libdir}/apps/
%dir %{_libdir}/apps/%{oname}
%{_libdir}/apps/%{oname}/Templates.glade
%{_libdir}/apps/%{oname}/.DirIcon
%{_libdir}/apps/%{oname}/A*
%{_libdir}/apps/%{oname}/Options.xml
%dir %{_libdir}/apps/%{oname}/Messages
%{_libdir}/apps/%{oname}/ROX*
%{_libdir}/apps/%{oname}/images
%{_libdir}/apps/%{oname}/style.css
%{_libdir}/apps/%{oname}/subclasses
#wrappers
%{_libdir}/apps/A*
%{_libdir}/apps/E*
%{_libdir}/apps/G*
%{_libdir}/apps/L*
%{_libdir}/apps/M*
%{_libdir}/apps/N*
%{_libdir}/apps/O*
%{_libdir}/apps/README
%{_libdir}/apps/S*
%{_libdir}/apps/T*
%{_libdir}/apps/V*
%{_libdir}/apps/X*
%{_mandir}/man1/*
%{_bindir}/*
%dir %{_datadir}/Choices
%dir %{_datadir}/Choices/MIME-types
%{_datadir}/mime/packages/rox.xml
%{_liconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_datadir}/applications/mandriva-*


