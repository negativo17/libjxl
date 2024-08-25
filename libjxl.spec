Name:       libjxl
Version:    0.10.3
Release:    1%{?dist}
Summary:    JPEG XL image format reference implementation
License:    BSD-3-Clause
URL:        https://github.com/libjxl/%{name}

Source0:    %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  asciidoc
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  giflib-devel >= 5.1
BuildRequires:  gmock-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel >= 1.6.40
BuildRequires:  pkgconfig(gdk-2.0)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0) >= 2.36
BuildRequires:  pkgconfig(gimp-2.0) >= 2.10
BuildRequires:  pkgconfig(gimpui-2.0) >= 2.10
BuildRequires:  pkgconfig(libhwy) >= 1.0.7
BuildRequires:  pkgconfig(libavif)
BuildRequires:  pkgconfig(libbrotlidec)
BuildRequires:  pkgconfig(libbrotlienc)
BuildRequires:  pkgconfig(libtcmalloc_minimal)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(lcms2) >= 2.12
BuildRequires:  pkgconfig(OpenEXR)
BuildRequires:  xdg-utils
# Actually zlib-ng-compat-devel:
BuildRequires:  pkgconfig(zlib) >= 1.3.1

# 6000+ tests take also very long to complete, and they also require additional
# /testdata at https://github.com/libjxl/testdata
%if %{with tests}
BuildRequires:  gtest-devel
%endif

# Build libjpeg.so shared library based on jpegli and install it as a
# replacement of libjpeg.so. Development of jpegli seems now to be out of tree:
# https://github.com/google/jpegli
%if %{with jpegli}
BuildRequires:  turbojpeg-devel >= 2.1.5.1
%endif

%description
JPEG XL image format reference implementation Library.

JPEG XL was standardized in 2022 as ISO/IEC 18181. The core codestream is
specified in 18181-1, the file format in 18181-2. Decoder conformance is defined
in 18181-3, and 18181-4 is the reference software.

%package -n jxl-pixbuf-loader
Summary: JPEG XL image loader for GTK+ applications

%description -n jxl-pixbuf-loader
This package provides JPEG XL image loader for gdk-pixbuf.

%package devel
Summary:    Development files for %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package tools
Summary:    The JPEG XL library command line tools

%description tools
This package provides JPEG XL tools.

%package -n gimp-%{name}-plugin
Summary:    JPEG XL plugin for GIMP
Requires:   gimp >= 2
Requires:   gimp < 3

%description -n gimp-%{name}-plugin
This package provides JPEG XL support for GIMP.

%prep
%autosetup

%build
%cmake \
  -DJPEGXL_BUNDLE_LIBPNG=FALSE \
  -DJPEGXL_ENABLE_AVX512=TRUE \
  -DJPEGXL_ENABLE_AVX512_SPR=TRUE \
  -DJPEGXL_ENABLE_AVX512_ZEN4=TRUE \
  -DJPEGXL_ENABLE_BENCHMARK=TRUE \
  -DJPEGXL_ENABLE_BOXES=TRUE \
  -DJPEGXL_ENABLE_COVERAGE=FALSE \
  -DJPEGXL_ENABLE_DEVTOOLS=FALSE \
  -DJPEGXL_ENABLE_DOXYGEN=TRUE \
  -DJPEGXL_ENABLE_EXAMPLES=TRUE \
  -DJPEGXL_ENABLE_FUZZERS=FALSE \
  -DJPEGXL_ENABLE_JNI=TRUE \
%if %{with jpegli}
  -DJPEGXL_ENABLE_JPEGLI=TRUE \
  -DJPEGXL_ENABLE_JPEGLI_LIBJPEG=TRUE \
  -DJPEGXL_INSTALL_JPEGLI_LIBJPEG=TRUE \
%endif
  -DJPEGXL_ENABLE_MANPAGES=TRUE \
  -DJPEGXL_ENABLE_OPENEXR=TRUE \
  -DJPEGXL_ENABLE_PLUGINS=TRUE \
  -DJPEGXL_ENABLE_SIZELESS_VECTORS=TRUE \
  -DJPEGXL_ENABLE_SJPEG=FALSE \
  -DJPEGXL_ENABLE_SKCMS=FALSE \
  -DJPEGXL_ENABLE_TCMALLOC=TRUE \
  -DJPEGXL_ENABLE_TOOLS=TRUE \
  -DJPEGXL_ENABLE_TRANSCODE_JPEG=TRUE \
  -DJPEGXL_ENABLE_VIEWERS=FALSE \
  -DJPEGXL_ENABLE_WASM_TRHEADS=TRUE \
  -DJPEGXL_FORCE_NEON=TRUE \
  -DJPEGXL_FORCE_SYSTEM_BROTLI=TRUE \
  -DJPEGXL_FORCE_SYSTEM_GTEST=TRUE \
  -DJPEGXL_FORCE_SYSTEM_HWY=TRUE \
  -DJPEGXL_FORCE_SYSTEM_LCMS2=TRUE \
  -DJPEGXL_STATIC=FALSE \
  -DJPEGXL_TEST_TOOLS=FALSE \
  -DJPEGXL_WARNINGS_AS_ERRORS=FALSE
%cmake_build

%install
%cmake_install

%if %{with tests}
%check
%cmake_build -t test
%endif

%files
%{_libdir}/%{name}.so.*
%{_libdir}/%{name}_cms.so.*
%{_libdir}/%{name}_extras_codec.so.*
%{_libdir}/%{name}_threads.so.*
%doc AUTHORS README* PATENTS

%files -n jxl-pixbuf-loader
%{_libdir}/gdk-pixbuf-2.0/*/loaders/libpixbufloader-jxl.so
%{_datadir}/thumbnailers/jxl.thumbnailer
%{_datadir}/mime/packages/image-jxl.xml

%files -n gimp-%{name}-plugin
%{_libdir}/gimp/2.0/plug-ins/file-jxl/file-jxl

%files devel
%{_includedir}/jxl/
%{_libdir}/%{name}.so
%{_libdir}/%{name}_cms.so
%{_libdir}/%{name}_extras_codec.so
%{_libdir}/%{name}_threads.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}_cms.pc
%{_libdir}/pkgconfig/%{name}_threads.pc

%files tools
%{_bindir}/benchmark_xl
%{_bindir}/cjxl
%{_bindir}/djxl
%{_bindir}/jxlinfo
%if %{with jpegli}
%{_bindir}/cjpegli
%{_bindir}/djpegli
%endif
%{_mandir}/man1/cjxl.1*
%{_mandir}/man1/djxl.1*

%changelog
* Sun Aug 25 2024 Simone Caronni <negativo17@gmail.com> - 0.10.3-1
- First build.
