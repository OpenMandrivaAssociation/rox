%define wrappers_ver	1.0.3
%define oname ROX-Filer

Name:		rox
Version: 	2.6.1
Release: %mkrel 1
Summary:	A fast and powerful graphical file manager
Group:		Graphical desktop/Other
License:	GPL
URL:		http://rox.sourceforge.net
Source:		http://prdownloads.sourceforge.net/%{name}/%{name}-filer-%{version}.tar.bz2
Source1:	http://prdownloads.sourceforge.net/%{name}/Wrappers-%{wrappers_ver}.tar.bz2
Source2:	rox-48.png
Source3:	rox-32.png
Source4:	rox-16.png
Patch0:		rox-20040801-xvt.patch
Patch1:		rox-2.1.2-shell.patch
Patch2:		rox-2.1.0-gnuclient.patch
Provides:	rox-base
Obsoletes:	rox-base
BuildRoot:	%{_tmppath}/%{name}-%version-buildroot
BuildRequires:	libgtk+2.0-devel >= 2.2.0
BuildRequires:  libxml2-devel
BuildRequires:  libgnome-vfs2-devel >= 2.8.0
BuildRequires:  libxt-devel
Requires(pre):	shared-mime-info >= 0.14
Requires(post):	shared-mime-info >= 0.14

%description
ROX-Filer is a fast, powerful, and easy to use graphical file
manager. It has full support for drag-and-drop and application
directories.  The filer can also provide a pinboard (allowing you to pin
up files on your desktop background) and panels.  The emphasis is on
uncluttered directory views; menus and prompts only appear when needed.

The Wrappers package found on the Rox home page is already included.

%prep
%setup -q -a 1 -n rox-filer-%version
%patch0 -p1
%patch1 -p1 -b .shell
%patch2 -p1 -b .gnuclient

%build
export CFLAGS="$RPM_OPT_FLAGS -I%_prefix/X11R6/lib"
./%oname/AppRun --compile

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%_libdir/apps
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_datadir}/mime/packages
cp -a %oname $RPM_BUILD_ROOT%_libdir/apps/
rm -rf $RPM_BUILD_ROOT%_libdir/apps/src
rm -rf $RPM_BUILD_ROOT%_libdir/apps/*/{src,build}
cp -a rox.1 $RPM_BUILD_ROOT%{_mandir}/man1
( cd $RPM_BUILD_ROOT%{_mandir}/man1 ; ln -s rox.1 %oname.1 )
cat << EOF > $RPM_BUILD_ROOT%{_bindir}/rox
#!/bin/sh
exec %_libdir/apps/%oname/AppRun "\$@"
EOF
chmod a+x $RPM_BUILD_ROOT%{_bindir}/rox
cp rox.xml $RPM_BUILD_ROOT%{_datadir}/mime/packages
cp -r Choices $RPM_BUILD_ROOT%{_datadir}

# Wrappers
cp -a Wrappers/* $RPM_BUILD_ROOT%_libdir/apps/
cp -a Wrappers/README README.wrappers

# desktop entry
mkdir -p $RPM_BUILD_ROOT%{_datadir}/gnome/apps/Applications
cat > $RPM_BUILD_ROOT%{_datadir}/gnome/apps/Applications/%{name}.desktop <<EOF
[Desktop Entry]
Name=ROX Filer
Comment=ROX Filer
Exec=rox
Icon=rox
Terminal=false
MultipleArgs=false
Type=Application
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
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


install -D %{SOURCE2} $RPM_BUILD_ROOT%{_liconsdir}/%name.png
install -D %{SOURCE3} $RPM_BUILD_ROOT%{_iconsdir}/%name.png
install -D %{SOURCE4} $RPM_BUILD_ROOT%{_miconsdir}/%name.png

# remove temp file
rm -f $RPM_BUILD_ROOT%_libdir/apps/Netscape/.AppRun.swp $RPM_BUILD_ROOT%{_datadir}/Choices/MIME-types/* $RPM_BUILD_ROOT%_libdir/apps/ROX-Filer/AppRun.*

for gmo in %buildroot%_libdir/apps/%oname/Messages/*.gmo;do
echo "%lang($(basename $gmo|sed s/.gmo//)) $(echo $gmo|sed s!%buildroot!!)" >> %name.lang
done

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_mime_database

%postun
%clean_mime_database

%files -f %name.lang
%defattr (-,root,root)
%doc README*
%doc %_libdir/apps/%oname/Help
%doc %_libdir/apps/%oname/Messages/README
%dir %_libdir/apps/
%dir %_libdir/apps/%oname
%_libdir/apps/%oname/.DirIcon
%_libdir/apps/%oname/A*
%_libdir/apps/%oname/Options.xml
%dir %_libdir/apps/%oname/Messages
%_libdir/apps/%oname/ROX*
%_libdir/apps/%oname/images
%_libdir/apps/%oname/style.css
%_libdir/apps/%oname/subclasses
#wrappers
%_libdir/apps/A*
%_libdir/apps/E*
%_libdir/apps/G*
%_libdir/apps/L*
%_libdir/apps/M*
%_libdir/apps/N*
%_libdir/apps/O*
%_libdir/apps/README
%_libdir/apps/S*
%_libdir/apps/T*
%_libdir/apps/V*
%_libdir/apps/X*
%{_mandir}/man1/*
%{_bindir}/*
%{_datadir}/gnome/apps/Applications/%{name}.desktop
%dir %{_datadir}/Choices
%dir %{_datadir}/Choices/MIME-types
%{_datadir}/mime/packages/rox.xml
%_liconsdir/%name.png
%_iconsdir/%name.png
%_miconsdir/%name.png
%_datadir/applications/mandriva-*


