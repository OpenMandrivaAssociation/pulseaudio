# pulseaudio is used by wine and some of its dependencies
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%define fullgit f81e3e1d7852c05b4b737ac7dac4db95798f0117
#define git 0

%bcond_with bootstrap

# (cg) Lennart has introduced a circular dependancy in the libraries
# libpulse requires libpulsecommon but libpulsecommon requires libpulse.
# This breaks no-undefined.
# Further issues in some test apps (maybe more) require that disabling
# as-needed is also required.
%define _disable_ld_no_undefined 1
%global __requires_exclude devel\\(libpulsecommon

# src/pulsecore/sink-input.c:1508:59: warning: dereferencing type-punned pointer might break strict-aliasing rules
%global optflags %{optflags} -O3 -fno-strict-aliasing

# Majors
%define major 0
%define glib2major 0
%define apiver %(echo %{version} |cut -d. -f1-2)

# Library names
%define libname %mklibname %{name}
%define devname %mklibname -d %{name}

%define glib2libname %mklibname pulseglib2

%define lib32name lib%{name}
%define dev32name lib%{name}-devel
%define glib2lib32name libpulseglib2

Summary:	Sound server for Linux
Name:		pulseaudio
Version:	16.1
Release:	7
License:	LGPLv2+
Group:		Sound
Url:		http://pulseaudio.org/
#Source0:	%{name}-%{version}%{?git:-%{git}}.tar.xz
Source0:	http://freedesktop.org/software/pulseaudio/releases/%{name}-%{version}%{?git:-%{fullgit}}.tar.xz
Source1:	%{name}.sysconfig
Source4:	%{name}.svg
Source10:	pavucontrol
# Load more modules if they are available
Patch0:		pulseaudio-5.0-defaults.patch
Patch1:		pulseaudio-6.0-kde-delay.patch
Patch2:		pulseaudio-13.99.1-non-x86.patch
# Load device-manager module
Patch3:		pulseaudio-7.1-load-module-device-manager.patch
# OM MODIFIED VERSION: Rebased to 14.99.2
Patch4:		https://gitlab.freedesktop.org/pulseaudio/pulseaudio/-/merge_requests/395.patch
Patch5:		https://src.fedoraproject.org/rpms/pulseaudio/raw/rawhide/f/pulseaudio-11.1-autospawn_disable.patch
Patch503:	https://raw.githubusercontent.com/clearlinux-pkgs/pulseaudio/master/lessfence.patch
Patch504:	https://raw.githubusercontent.com/clearlinux-pkgs/pulseaudio/master/memfd.patch
BuildRequires:	meson
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	imagemagick
BuildRequires:	intltool >= 0.51.0
BuildRequires:	libtool
BuildRequires:	pkgconfig(libcap)
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(atomic_ops)
BuildRequires:	libtool-devel
BuildRequires:	wrap-devel
BuildRequires:	valgrind-devel
BuildRequires:	pkgconfig(check)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(avahi-client)
BuildRequires:	avahi-common-devel
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(json-c)
BuildRequires:	pkgconfig(ldacBT-enc)
BuildRequires:	pkgconfig(ldacBT-abr)
BuildRequires:	pkgconfig(libfreeaptx)
BuildRequires:	pkgconfig(libopenaptx)
BuildRequires:	pkgconfig(libasyncns)
BuildRequires:	pkgconfig(liblircclient0)
BuildRequires:	pkgconfig(webrtc-audio-processing-1)
BuildRequires:	cmake(absl)
BuildRequires:	pkgconfig(sbc)
BuildRequires:	pkgconfig(soxr)
# (cg) Needed for airtunes
BuildRequires:	pkgconfig(libssl)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(udev) >= 186
BuildRequires:	pkgconfig(orc-0.4)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(speexdsp)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(tdb)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(x11-xcb)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pkgconfig(xcb-util)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(bash-completion)
%if !%{with bootstrap}
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(gstreamer-app-1.0)
%endif
%rename		pulseaudio-module-xen
%rename		polypaudio
Requires:	rtkit
Requires(post):	ccp
%systemd_requires
# (cg) When upgrading from pa < 0.9.7-1 things break due to spec restructure
Conflicts:	%{libname} < 0.9.7-2
Obsoletes:	%{mklibname pulsezeroconf 0} < 1.0
# (cg) libpulsecore has been moved to a dlopen'ed system.
Obsoletes:	%{mklibname pulsecore 1} < 16.1
Obsoletes:	%{mklibname pulsecore 2} < 16.1
Obsoletes:	%{mklibname pulsecore 3} < 16.1
Obsoletes:	%{mklibname pulsecore 4} < 16.1
Obsoletes:	%{mklibname pulsecore 5} < 16.1
Obsoletes:	%{mklibname pulsecore 6} < 16.1
Obsoletes:	%{mklibname pulsecore 7} < 16.1
Obsoletes:	%{mklibname pulsecore 8} < 16.1
Obsoletes:	%{mklibname pulsecore 7.0} < 8.0
Obsoletes:	%{mklibname pulsecore 7.1} < 8.0
Provides:	%{mklibname pulsecore 7.0} = 8.0
Provides:	%{mklibname pulsecore 7.1} = 8.0
Obsoletes:	%{mklibname pulsezeroconf 0} < 16.1
Conflicts:	%{libname} < 5.0
Obsoletes:	%{mklibname pulsecommon 7.0} < 8.0
Obsoletes:	%{mklibname pulsecommon 7.1} < 8.0
Provides:	%{mklibname pulsecommon 7.0} = 8.0
Provides:	%{mklibname pulsecommon 7.1} = 8.0
Provides:	%{mklibname pulsecommon 5.0}

%if %{with compat32}
BuildRequires:	devel(libatomic_ops)
BuildRequires:	devel(libasound)
BuildRequires:	devel(libltdl)
BuildRequires:	devel(libsndfile)
BuildRequires:	devel(libcheck)
BuildRequires:	devel(libtdb)
BuildRequires:	devel(liborc-0.4)
BuildRequires:	devel(libsoxr)
BuildRequires:	devel(libxml2)
BuildRequires:	devel(libxslt)
BuildRequires:	devel(libXtst)
BuildRequires:	devel(libdaemon)
BuildRequires:	devel(libsbc)
BuildRequires:	devel(libbluetooth)
BuildRequires:	devel(libfftw3f)
BuildRequires:	devel(libavahi-client)
BuildRequires:	devel(libjack)
BuildRequires:	devel(libspeex)
BuildRequires:	devel(libspeexdsp)
BuildRequires:	devel(libdbus-1)
BuildRequires:	devel(libgio-2.0)
BuildRequires:	devel(libgobject-2.0)
BuildRequires:	devel(libffi)
BuildRequires:	devel(libmount)
BuildRequires:	devel(libblkid)
BuildRequires:	devel(libsystemd)
BuildRequires:	devel(libsamplerate)
BuildRequires:	devel(libX11-xcb)
BuildRequires:	devel(libxcb)
BuildRequires:	devel(libcap)
BuildRequires:	devel(libXau)
BuildRequires:	devel(libXdmcp)
BuildRequires:	devel(libICE)
BuildRequires:	devel(libSM)
BuildRequires:	devel(libXtst)
BuildRequires:	devel(libXi)
BuildRequires:	devel(libXfixes)
BuildRequires:	devel(libXext)
BuildRequires:	devel(libssl)
BuildRequires:	devel(libudev)
%endif

%description
pulseaudio is a sound server for Linux and other Unix like operating
systems. It is intended to be an improved drop-in replacement for the
Enlightened Sound Daemon (EsounD). In addition to the features EsounD
provides pulseaudio has:
     * Extensible plugin architecture (by loading dynamic loadable
       modules with dlopen())
     * Support for more than one sink/source
     * Better low latency behaviour
     * Embedabble into other software (the core is available as C
       library)
     * Completely asynchronous C API
     * Simple command line interface for reconfiguring the daemon while
       running
     * Flexible, implicit sample type conversion and resampling
     * "Zero-Copy" architecture
     * Module autoloading
     * Very accurate latency measurement for playback and recording.
     * May be used to combine multiple sound cards to one (with sample
       rate adjustment)
     * Client side latency interpolation

%package -n %{libname}
Summary:	Libraries for PulseAudio clients
Group:		System/Libraries
Requires:	%{name}-client-config
%rename %{mklibname %{name} 0}

%description -n %{libname}
This package contains the runtime libraries for any application that wishes
to interface with a PulseAudio sound server.

%define alt_name soundprofile
%define alt_priority 20

%package client-config
Summary:	Client configuration for PulseAudio clients
Group:		System/Libraries
# (proyvind): leave thix as suggests, do not change into requires, otherwise
#             pulseaudio cannot be disabled by default
Suggests:	%{mklibname alsa-plugins}-pulseaudio
Requires(post):	ccp
Requires(post):	chkconfig
Requires(postun):	chkconfig
Conflicts:	%{name} < 0.9.16-0.20090816.1
# (cg) Adding the obsoletes here as this package is almost always installed
#      and doing it in task-pulseaudio would cause it to be installed when not needed.
# Flash plugin support pulse natively and libflashsupport now causes more
# problems than it fixes
Obsoletes:	libflashsupport

%description client-config
This package contains the client configuration files for any application that
wishes to interface with a PulseAudio sound server.

%package -n %{glib2libname}
Summary:	GLIB 2.x bindings for PulseAudio clients
Group:		System/Libraries
%rename %{mklibname pulseglib2 0}

%description -n %{glib2libname}
This package contains bindings to integrate the PulseAudio client library with
a GLIB 2.x based application.

%package -n %{devname}
Summary:	Headers and libraries for PulseAudio client development
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{glib2libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname -d %{name} %{major}

%description -n %{devname}
Headers and libraries for developing applications that can communicate with
a PulseAudio sound server.

%package module-gsettings
Summary:	Gsettings support for the PulseAudio sound server
Requires:	%{name}%{?_isa} = %{EVRD}
%rename	%{name}-module-gconf

%description module-gsettings
GSettings configuration backend for the PulseAudio sound server.

%package module-lirc
Summary:	LIRC support for the PulseAudio sound server
Group:		Sound
Requires:	%{name} = %{EVRD}

%description module-lirc
LIRC volume control module for the PulseAudio sound server.

%if !%{with bootstrap}
%package module-bluetooth
Summary:	Bluetooth support for the PulseAudio sound server
Group:		Sound
Requires:	%{name} = %{EVRD}

%description module-bluetooth
Bluetooth modules for the PulseAudio sound server to provide support
for headsets and proximity detection.
%endif

%package module-x11
Summary:	X11 support for the PulseAudio sound server
Group:		Sound
Requires:	%{name} = %{EVRD}
Requires:	%{name}-utils = %{EVRD}

%description module-x11
X11 bell and security modules for the PulseAudio sound server.

%package module-zeroconf
Summary:	Zeroconf support for the PulseAudio sound server
Group:		Sound
Requires:	%{name} = %{EVRD}

%description module-zeroconf
Zeroconf publishing module for the PulseAudio sound server.

%package module-jack
Summary:	JACK support for the PulseAudio sound server
Group:		Sound
Requires:	%{name} = %{EVRD}

%description module-jack
JACK sink and source modules for the PulseAudio sound server.

%package module-equalizer
Summary:	Equalizer support for the PulseAudio sound server
Group:		Sound
Requires:	%{name} = %{EVRD}

%description module-equalizer
Equalizer support and GUI for the PulseAudio sound server.

%package utils
Summary:	PulseAudio sound server utilities
Group:		Sound

%description utils
This package contains command line utilities for the PulseAudio sound server.

%package server
Summary:	PulseAudio server
Group:		Sound

%description server
The PulseAudio server.

Install %{name}-server if you don't want to use
pipewire-pulse.

%if %{with compat32}
%package -n %{lib32name}
Summary:	Libraries for PulseAudio clients (32-bit)
Group:		System/Libraries
Requires:	%{name}-client-config
%rename lib%{name}0

%description -n %{lib32name}
This package contains the runtime libraries for any application that wishes
to interface with a PulseAudio sound server.

%package -n %{glib2lib32name}
Summary:	GLIB 2.x bindings for PulseAudio clients (32-bit)
Group:		System/Libraries
%rename libpulseglib2_0

%description -n %{glib2lib32name}
This package contains bindings to integrate the PulseAudio client library with
a GLIB 2.x based application.

%package -n %{dev32name}
Summary:	Headers and libraries for PulseAudio client development (32-bit)
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}
Requires:	%{glib2lib32name} = %{version}-%{release}

%description -n %{dev32name}
Headers and libraries for developing applications that can communicate with
a PulseAudio sound server.
%endif

%prep
%autosetup -n %{name}-%{version}%{?git:-%{fullgit}} -p1
%if %{with compat32}
%meson32 \
	-Ddoxygen=false \
	-Dman=false \
	-Dtests=false \
	-Dvalgrind=disabled \
	-Dhal-compat=false \
	-Dgtk=disabled \
	-Dasyncns=disabled \
	-Dlirc=disabled \
	-Dwebrtc-aec=disabled \
	-Dgstreamer=disabled \
	-Dbluez5-gstreamer=disabled \
	-Dsystemd=disabled \
	-Dudev=disabled \
	-Delogind=disabled \
	-Dtcpwrap=disabled \
	-Dudevrulesdir=%{_udevrulesdir}
%endif

%ifarch %{arm}
# https://bugs.llvm.org/show_bug.cgi?id=48797
export CC=gcc
export CXX=g++
%endif

%meson \
	-Dtests=false \
	-Dcpp_std=gnu++17 \
	-Dhal-compat=false \
	-Dsystemd=enabled \
	-Dudevrulesdir=%{_udevrulesdir} \
	-Delogind=disabled \
	-Dbluez5=enabled \
	-Dbluez5-gstreamer=enabled \
	-Dbluez5-native-headset=true \
	-Dbluez5-ofono-headset=true \
	-Dadrian-aec=true \
	-Dwebrtc-aec=enabled \
%ifarch %{armx}
	-Datomic-arm-linux-helpers=true \
	-Datomic-arm-memory-barrier=true \
%endif
%if %{with bootstrap}
	-Dgstreamer=disabled
%else
	-Dgstreamer=enabled
%endif

%build
%if %{with compat32}
%ninja_build -C build32
rm -rf %{buildroot}%{_includedir}/*
rm -rf %{buildroot}%{_bindir}/*
rm -rf %{buildroot}%{_sysconfdir}/*
rm -rf %{buildroot}%{_datadir}/*
rm -rf %{buildroot}%{_udevrulesdir}/*
%endif
%ninja_build -C build

%install
%if %{with compat32}
%ninja_install -C build32
%endif
%ninja_install -C build

install -D -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -D -m 0644 %{SOURCE4} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/devices
ln -s ../apps/%{name}.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/devices/audio-backend-pulseaudio.svg
for size in 16 22 32 48 64 128; do
  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/{apps,devices}
  convert -geometry ${size}x${size} %{SOURCE4} %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/%{name}.png
  ln -s ../apps/%{name}.png %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/devices/audio-backend-pulseaudio.png
done

# (cg) For sound profile support
mkdir -p %{buildroot}%{_sysconfdir}/sound/profiles/pulse
echo "SOUNDPROFILE=pulse" >%{buildroot}%{_sysconfdir}/sound/profiles/pulse/profile.conf

# (cg) HAL support is no longer the default, and we don't officially support system wide, so
# System Wide + HAL is pretty unlikely.
rm -f %{buildroot}%{_sysconfdir}/dbus-1/system.d/%{name}-system.conf

# (cg) We require systemd now, so no point in using CK
rm -f %{buildroot}%{_libdir}/pulseaudio/modules/module-console-kit.so

# (cg) Disable x11-cork-request... it should be ahndled in the apps as we cannot
#      maintain state via this mechanism. Should be a patch, but I'm lazy.
sed -i 's,\(/usr/bin/pactl load-module module-x11-cork-request\),#\1,' %{buildroot}%{_bindir}/start-pulseaudio-x11

# Speed up pulseaudio shutdown so that it exits immediately with
# the last user session (module-systemd-login keeps it alive)
sed -e "/exit-idle-time/iexit-idle-time=0" -i %{buildroot}%{_sysconfdir}/pulse/daemon.conf

# (tpg) enable pulseaudio in userland
mkdir -p %{buildroot}%{_userunitdir}/sockets.target.wants
ln -sf %{_userunitdir}/pulseaudio.socket %{buildroot}%{_userunitdir}/sockets.target.wants/pulseaudio.socket

# Install the toolkit neutral pavucontrol wrapper
install -c -m 755 %{S:10} %{buildroot}%{_bindir}/pavucontrol

%find_lang %{name}

%post
ccp -i -d --set NoOrphans --oldfile %{_sysconfdir}/pulse/daemon.conf --newfile %{_sysconfdir}/pulse/daemon.conf.rpmnew

%post server
%systemd_user_post pulseaudio.socket

%preun server
%systemd_user_preun pulseaudio.socket

%postun server
%systemd_user_postun pulseaudio.socket

%post client-config
%{_sbindir}/update-alternatives \
  --install %{_sysconfdir}/sound/profiles/current %{alt_name} %{_sysconfdir}/sound/profiles/pulse %{alt_priority}
ccp -i -d --set NoOrphans --oldfile %{_sysconfdir}/pulse/client.conf --newfile %{_sysconfdir}/pulse/client.conf.rpmnew

%postun client-config
if [ ! -f %{_sysconfdir}/sound/profiles/pulse/profile.conf ]; then
  /usr/sbin/update-alternatives --remove %{alt_name} %{_sysconfdir}/sound/profiles/pulse
fi

%triggerin client-config -- %{name}-client-config < 6.0-3
# Autospawn behaviour changed to use systemd, so tidy up the client.conf
# by setting it back to the default value - it no longer changes depending on
# the users soundprofile choice - it always defaults to no.
sed -i 's/^\(\s*\)\;\?\s*\(autospawn\s*=\s*\).*/\1\; \2no/' %{_sysconfdir}/pulse/client.conf

%files -f %{name}.lang
%doc README
%dir %{_sysconfdir}/pulse/
%config(noreplace) %{_sysconfdir}/pulse/daemon.conf
%config(noreplace) %{_sysconfdir}/pulse/default.pa
%config(noreplace) %{_sysconfdir}/pulse/system.pa
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_bindir}/pa-info
%{_bindir}/pavucontrol
%doc %{_mandir}/man5/pulse-client.conf.5.*
%doc %{_mandir}/man5/pulse-daemon.conf.5.*
%doc %{_mandir}/man5/default.pa.5.*
%doc %{_mandir}/man5/pulse-cli-syntax.5.*
%{_datadir}/icons/hicolor/*/*/*
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/alsa-mixer
%{_udevrulesdir}/90-pulseaudio.rules

%files server
%{_bindir}/%{name}
%doc %{_mandir}/man1/%{name}.1.*
%{_datadir}/zsh/site-functions/_pulseaudio
%{_userunitdir}/pulseaudio.service
%{_userunitdir}/pulseaudio.socket
%{_userunitdir}/sockets.target.wants/pulseaudio.socket

%files -n %{libname}
%{_libdir}/libpulse.so.%{major}*
%{_libdir}/libpulse-simple.so.%{major}*
# Modules go to the library package because 32-bit versions of the libraries
# require 32-bit versions of the core modules.
%{_libdir}/%{name}/libpulsedsp.so
%{_libdir}/%{name}/libpulsecore-%{apiver}.so
%{_libdir}/%{name}/libpulsecommon-%{apiver}.so
%dir %{_libdir}/pulseaudio
%dir %{_libdir}/pulseaudio/modules/
%{_libdir}/pulseaudio/modules/module-allow-passthrough.so
%{_libdir}/pulseaudio/modules/libalsa-util.so
%{_libdir}/pulseaudio/modules/liboss-util.so
%{_libdir}/pulseaudio/modules/libcli.so
%{_libdir}/pulseaudio/modules/libprotocol-cli.so
%{_libdir}/pulseaudio/modules/libprotocol-http.so
%{_libdir}/pulseaudio/modules/libprotocol-native.so
%{_libdir}/pulseaudio/modules/libprotocol-simple.so
%{_libdir}/pulseaudio/modules/libraop.so
%{_libdir}/pulseaudio/modules/librtp.so
%{_libdir}/pulseaudio/modules/libwebrtc-util.so
%{_libdir}/pulseaudio/modules/module-always-source.so
%{_libdir}/pulseaudio/modules/module-alsa-card.so
%{_libdir}/pulseaudio/modules/module-alsa-sink.so
%{_libdir}/pulseaudio/modules/module-alsa-source.so
%{_libdir}/pulseaudio/modules/module-oss.so
%{_libdir}/pulseaudio/modules/module-always-sink.so
%{_libdir}/pulseaudio/modules/module-augment-properties.so
%{_libdir}/pulseaudio/modules/module-card-restore.so
%{_libdir}/pulseaudio/modules/module-cli-protocol-tcp.so
%{_libdir}/pulseaudio/modules/module-cli-protocol-unix.so
%{_libdir}/pulseaudio/modules/module-cli.so
%{_libdir}/pulseaudio/modules/module-combine.so
%{_libdir}/pulseaudio/modules/module-combine-sink.so
%{_libdir}/pulseaudio/modules/module-role-cork.so
%{_libdir}/pulseaudio/modules/module-systemd-login.so
%{_libdir}/pulseaudio/modules/module-dbus-protocol.so
%{_libdir}/pulseaudio/modules/module-detect.so
%{_libdir}/pulseaudio/modules/module-device-manager.so
%{_libdir}/pulseaudio/modules/module-device-restore.so
%{_libdir}/pulseaudio/modules/module-echo-cancel.so
#%{_libdir}/pulseaudio/modules/module-hal-detect.so
%{_libdir}/pulseaudio/modules/module-http-protocol-tcp.so
%{_libdir}/pulseaudio/modules/module-http-protocol-unix.so
%{_libdir}/pulseaudio/modules/module-intended-roles.so
%{_libdir}/pulseaudio/modules/module-loopback.so
%{_libdir}/pulseaudio/modules/module-match.so
%{_libdir}/pulseaudio/modules/module-mmkbd-evdev.so
%{_libdir}/pulseaudio/modules/module-native-protocol-fd.so
%{_libdir}/pulseaudio/modules/module-native-protocol-tcp.so
%{_libdir}/pulseaudio/modules/module-native-protocol-unix.so
%{_libdir}/pulseaudio/modules/module-null-sink.so
%{_libdir}/pulseaudio/modules/module-null-source.so
%{_libdir}/pulseaudio/modules/module-pipe-sink.so
%{_libdir}/pulseaudio/modules/module-pipe-source.so
%{_libdir}/pulseaudio/modules/module-raop-sink.so
%{_libdir}/pulseaudio/modules/module-rygel-media-server.so
%{_libdir}/pulseaudio/modules/module-position-event-sounds.so
%{_libdir}/pulseaudio/modules/module-rescue-streams.so
%{_libdir}/pulseaudio/modules/module-rtp-recv.so
%{_libdir}/pulseaudio/modules/module-rtp-send.so
%{_libdir}/pulseaudio/modules/module-simple-protocol-tcp.so
%{_libdir}/pulseaudio/modules/module-simple-protocol-unix.so
%{_libdir}/pulseaudio/modules/module-sine.so
%{_libdir}/pulseaudio/modules/module-sine-source.so
%{_libdir}/pulseaudio/modules/module-tunnel-sink.so
%{_libdir}/pulseaudio/modules/module-tunnel-source.so
%{_libdir}/pulseaudio/modules/module-tunnel-sink-new.so
%{_libdir}/pulseaudio/modules/module-tunnel-source-new.so
%{_libdir}/pulseaudio/modules/module-udev-detect.so
%{_libdir}/pulseaudio/modules/module-volume-restore.so
%{_libdir}/pulseaudio/modules/module-virtual-sink.so
%{_libdir}/pulseaudio/modules/module-virtual-source.so
%{_libdir}/pulseaudio/modules/module-stream-restore.so
%{_libdir}/pulseaudio/modules/module-suspend-on-idle.so
%{_libdir}/pulseaudio/modules/module-default-device-restore.so
%{_libdir}/pulseaudio/modules/module-ladspa-sink.so
%{_libdir}/pulseaudio/modules/module-remap-sink.so
%{_libdir}/pulseaudio/modules/module-remap-source.so
%{_libdir}/pulseaudio/modules/module-switch-on-connect.so
%{_libdir}/pulseaudio/modules/module-filter-apply.so
%{_libdir}/pulseaudio/modules/module-filter-heuristics.so
%{_libdir}/pulseaudio/modules/module-virtual-surround-sink.so
%{_libdir}/pulseaudio/modules/module-switch-on-port-available.so
%{_libdir}/pulseaudio/modules/module-role-ducking.so

%files client-config
%config(noreplace) %{_sysconfdir}/pulse/client.conf
%dir %{_sysconfdir}/sound/profiles/pulse
%{_sysconfdir}/sound/profiles/pulse/profile.conf

%files -n %{glib2libname}
%{_libdir}/libpulse-mainloop-glib.so.%{glib2major}*

%files -n %{devname}
%{_libdir}/libpulse.so
%{_libdir}/libpulse-mainloop-glib.so
%{_libdir}/libpulse-simple.so
%dir %{_includedir}/pulse
%{_includedir}/pulse/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/PulseAudio
%{_datadir}/vala/vapi/libpulse.deps
%{_datadir}/vala/vapi/libpulse.vapi
%{_datadir}/vala/vapi/libpulse-mainloop-glib.deps
%{_datadir}/vala/vapi/libpulse-mainloop-glib.vapi
%{_datadir}/vala/vapi/libpulse-simple.deps
%{_datadir}/vala/vapi/libpulse-simple.vapi

%files module-gsettings
%{_libdir}/pulseaudio/modules/module-gsettings.so
%{_libexecdir}/pulse/gsettings-helper
%{_datadir}/GConf/gsettings/pulseaudio.convert
%{_datadir}/glib-2.0/schemas/org.freedesktop.pulseaudio.gschema.xml

%if !%{with bootstrap}
%files module-bluetooth
%{_libdir}/pulseaudio/modules/libbluez5-util.so
%{_libdir}/pulseaudio/modules/module-bluetooth-discover.so
%{_libdir}/pulseaudio/modules/module-bluetooth-policy.so
%{_libdir}/pulseaudio/modules/module-bluez5-device.so
%{_libdir}/pulseaudio/modules/module-bluez5-discover.so
%endif

%files module-lirc
%{_libdir}/pulseaudio/modules/module-lirc.so

%files module-x11
%{_bindir}/pax11publish
%{_bindir}/start-pulseaudio-x11
%doc %{_mandir}/man1/pax11publish.1.*
%doc %{_mandir}/man1/start-pulseaudio-x11.1.*
%{_libdir}/pulseaudio/modules/module-x11-bell.so
%{_libdir}/pulseaudio/modules/module-x11-cork-request.so
%{_libdir}/pulseaudio/modules/module-x11-publish.so
%{_libdir}/pulseaudio/modules/module-x11-xsmp.so
%{_sysconfdir}/xdg/autostart/pulseaudio.desktop
%{_sysconfdir}/xdg/Xwayland-session.d/00-pulseaudio-x11
%{_prefix}/lib/systemd/user/pulseaudio-x11.service

%files module-zeroconf
%{_libdir}/pulseaudio/modules/libavahi-wrap.so
%{_libdir}/pulseaudio/modules/module-zeroconf-discover.so
%{_libdir}/pulseaudio/modules/module-zeroconf-publish.so
%{_libdir}/pulseaudio/modules/module-raop-discover.so

%files module-jack
%{_libdir}/pulseaudio/modules/module-jack-sink.so
%{_libdir}/pulseaudio/modules/module-jack-source.so
%{_libdir}/pulseaudio/modules/module-jackdbus-detect.so

%files module-equalizer
%{_bindir}/qpaeq
%{_libdir}/pulseaudio/modules/module-equalizer-sink.so

%files utils
%{_datadir}/bash-completion/completions/p*
%{_bindir}/pacat
%{_bindir}/pacmd
%{_bindir}/pactl
%{_bindir}/padsp
%{_bindir}/pamon
%{_bindir}/paplay
%{_bindir}/parec
%{_bindir}/parecord
%{_bindir}/pasuspender
%doc %{_mandir}/man1/pacat.1.*
%doc %{_mandir}/man1/pamon.1.*
%doc %{_mandir}/man1/parec.1.*
%doc %{_mandir}/man1/parecord.1.*
%doc %{_mandir}/man1/pacmd.1.*
%doc %{_mandir}/man1/pactl.1.*
%doc %{_mandir}/man1/padsp.1.*
%doc %{_mandir}/man1/paplay.1.*
%doc %{_mandir}/man1/pasuspender.1.*

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libpulse.so.%{major}*
%{_prefix}/lib/libpulse-simple.so.%{major}*
%dir %{_prefix}/lib/pulseaudio
%{_prefix}/lib/%{name}/libpulsedsp.so
%{_prefix}/lib/%{name}/libpulsecore-%{apiver}.so
%{_prefix}/lib/%{name}/libpulsecommon-%{apiver}.so
%dir %{_prefix}/lib/pulseaudio/modules/
%{_prefix}/lib/pulseaudio/modules/module-allow-passthrough.so
%{_prefix}/lib/pulseaudio/modules/libalsa-util.so
%{_prefix}/lib/pulseaudio/modules/liboss-util.so
%{_prefix}/lib/pulseaudio/modules/libcli.so
%{_prefix}/lib/pulseaudio/modules/libprotocol-cli.so
%{_prefix}/lib/pulseaudio/modules/libprotocol-http.so
%{_prefix}/lib/pulseaudio/modules/libprotocol-native.so
%{_prefix}/lib/pulseaudio/modules/libprotocol-simple.so
%{_prefix}/lib/pulseaudio/modules/libraop.so
%{_prefix}/lib/pulseaudio/modules/librtp.so
%{_prefix}/lib/pulseaudio/modules/module-always-source.so
%{_prefix}/lib/pulseaudio/modules/module-alsa-card.so
%{_prefix}/lib/pulseaudio/modules/module-alsa-sink.so
%{_prefix}/lib/pulseaudio/modules/module-alsa-source.so
%{_prefix}/lib/pulseaudio/modules/module-oss.so
%{_prefix}/lib/pulseaudio/modules/module-always-sink.so
%{_prefix}/lib/pulseaudio/modules/module-augment-properties.so
%{_prefix}/lib/pulseaudio/modules/module-card-restore.so
%{_prefix}/lib/pulseaudio/modules/module-cli-protocol-tcp.so
%{_prefix}/lib/pulseaudio/modules/module-cli-protocol-unix.so
%{_prefix}/lib/pulseaudio/modules/module-cli.so
%{_prefix}/lib/pulseaudio/modules/module-combine.so
%{_prefix}/lib/pulseaudio/modules/module-combine-sink.so
%{_prefix}/lib/pulseaudio/modules/module-role-cork.so
#%{_prefix}/lib/pulseaudio/modules/module-systemd-login.so
%{_prefix}/lib/pulseaudio/modules/module-dbus-protocol.so
%{_prefix}/lib/pulseaudio/modules/module-detect.so
%{_prefix}/lib/pulseaudio/modules/module-device-manager.so
%{_prefix}/lib/pulseaudio/modules/module-device-restore.so
%{_prefix}/lib/pulseaudio/modules/module-echo-cancel.so
#%{_prefix}/lib/pulseaudio/modules/module-hal-detect.so
%{_prefix}/lib/pulseaudio/modules/module-http-protocol-tcp.so
%{_prefix}/lib/pulseaudio/modules/module-http-protocol-unix.so
%{_prefix}/lib/pulseaudio/modules/module-intended-roles.so
%{_prefix}/lib/pulseaudio/modules/module-loopback.so
%{_prefix}/lib/pulseaudio/modules/module-match.so
%{_prefix}/lib/pulseaudio/modules/module-mmkbd-evdev.so
%{_prefix}/lib/pulseaudio/modules/module-native-protocol-fd.so
%{_prefix}/lib/pulseaudio/modules/module-native-protocol-tcp.so
%{_prefix}/lib/pulseaudio/modules/module-native-protocol-unix.so
%{_prefix}/lib/pulseaudio/modules/module-null-sink.so
%{_prefix}/lib/pulseaudio/modules/module-null-source.so
%{_prefix}/lib/pulseaudio/modules/module-pipe-sink.so
%{_prefix}/lib/pulseaudio/modules/module-pipe-source.so
%{_prefix}/lib/pulseaudio/modules/module-raop-sink.so
%{_prefix}/lib/pulseaudio/modules/module-rygel-media-server.so
%{_prefix}/lib/pulseaudio/modules/module-position-event-sounds.so
%{_prefix}/lib/pulseaudio/modules/module-rescue-streams.so
%{_prefix}/lib/pulseaudio/modules/module-rtp-recv.so
%{_prefix}/lib/pulseaudio/modules/module-rtp-send.so
%{_prefix}/lib/pulseaudio/modules/module-simple-protocol-tcp.so
%{_prefix}/lib/pulseaudio/modules/module-simple-protocol-unix.so
%{_prefix}/lib/pulseaudio/modules/module-sine.so
%{_prefix}/lib/pulseaudio/modules/module-sine-source.so
%{_prefix}/lib/pulseaudio/modules/module-tunnel-sink.so
%{_prefix}/lib/pulseaudio/modules/module-tunnel-source.so
%{_prefix}/lib/pulseaudio/modules/module-tunnel-sink-new.so
%{_prefix}/lib/pulseaudio/modules/module-tunnel-source-new.so
#%{_prefix}/lib/pulseaudio/modules/module-udev-detect.so
%{_prefix}/lib/pulseaudio/modules/module-volume-restore.so
%{_prefix}/lib/pulseaudio/modules/module-virtual-sink.so
%{_prefix}/lib/pulseaudio/modules/module-virtual-source.so
%{_prefix}/lib/pulseaudio/modules/module-stream-restore.so
%{_prefix}/lib/pulseaudio/modules/module-suspend-on-idle.so
%{_prefix}/lib/pulseaudio/modules/module-default-device-restore.so
%{_prefix}/lib/pulseaudio/modules/module-ladspa-sink.so
%{_prefix}/lib/pulseaudio/modules/module-remap-sink.so
%{_prefix}/lib/pulseaudio/modules/module-remap-source.so
%{_prefix}/lib/pulseaudio/modules/module-switch-on-connect.so
%{_prefix}/lib/pulseaudio/modules/module-filter-apply.so
%{_prefix}/lib/pulseaudio/modules/module-filter-heuristics.so
%{_prefix}/lib/pulseaudio/modules/module-virtual-surround-sink.so
%{_prefix}/lib/pulseaudio/modules/module-switch-on-port-available.so
%{_prefix}/lib/pulseaudio/modules/module-role-ducking.so
%{_prefix}/lib/pulseaudio/modules/libavahi-wrap.so
%{_prefix}/lib/pulseaudio/modules/libbluez5-util.so
%{_prefix}/lib/pulseaudio/modules/module-bluetooth-discover.so
%{_prefix}/lib/pulseaudio/modules/module-bluetooth-policy.so
%{_prefix}/lib/pulseaudio/modules/module-bluez5-device.so
%{_prefix}/lib/pulseaudio/modules/module-bluez5-discover.so
%{_prefix}/lib/pulseaudio/modules/module-console-kit.so
%{_prefix}/lib/pulseaudio/modules/module-equalizer-sink.so
%{_prefix}/lib/pulseaudio/modules/module-gsettings.so
%{_prefix}/lib/pulseaudio/modules/module-jack-sink.so
%{_prefix}/lib/pulseaudio/modules/module-jack-source.so
%{_prefix}/lib/pulseaudio/modules/module-jackdbus-detect.so
%{_prefix}/lib/pulseaudio/modules/module-raop-discover.so
%{_prefix}/lib/pulseaudio/modules/module-x11-bell.so
%{_prefix}/lib/pulseaudio/modules/module-x11-cork-request.so
%{_prefix}/lib/pulseaudio/modules/module-x11-publish.so
%{_prefix}/lib/pulseaudio/modules/module-x11-xsmp.so
%{_prefix}/lib/pulseaudio/modules/module-zeroconf-discover.so
%{_prefix}/lib/pulseaudio/modules/module-zeroconf-publish.so
# FIXME do we need those? (Not all dependencies built for 32-bit so far)
#{_prefix}/lib/pulseaudio/modules/libwebrtc-util.so

%files -n %{glib2lib32name}
%{_prefix}/lib/libpulse-mainloop-glib.so.%{glib2major}*

%files -n %{dev32name}
%{_prefix}/lib/libpulse.so
%{_prefix}/lib/libpulse-mainloop-glib.so
%{_prefix}/lib/libpulse-simple.so
%{_prefix}/lib/pkgconfig/*.pc
%{_prefix}/lib/cmake/PulseAudio
%endif
