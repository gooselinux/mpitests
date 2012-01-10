Summary: MPI Benchmarks and tests
Name: mpitests
Version: 3.2
Release: 2%{?dist}
License: BSD
Group: Applications
Source: mpitests-%{version}.tar.gz
Patch0: mpitests-2.0-make.patch
Provides: mpitests
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root
# mvapich2 only exists on these three arches
ExclusiveArch: i386 x86_64 ia64

%description
Set of popular MPI benchmarks:
IMB-2.3
Presta-1.4.0
OSU benchmarks ver 2.2

%package openmpi
Summary: MPI tests package compiled against openmpi
Group: Applications
BuildRequires: openmpi >= 1.4, openmpi-devel
%description openmpi
MPI test suite compiled against the openmpi package

%package mvapich
Summary: MPI tests package compiled against mvapich
Group: Applications
BuildRequires: mvapich-devel >= 1.2.0
%description mvapich
MPI test suite compiled against the mvapich package

%package mvapich2
Summary: MPI tests package compiled against mvapich2
Group: Applications
BuildRequires: mvapich2-devel >= 1.4
BuildRequires: librdmacm-devel, libibumad-devel
%description mvapich2
MPI test suite compiled against the mvapich2 package

%prep
%setup -q -a 0
# secretly patch the code one layer down, not at the top level
%patch0 -p0 -b .make

%build
rm -rf %{buildroot}
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-Wp,-D_FORTIFY_SOURCE=.//' | sed -e 's/-fstack-protector//'`
# We don't do a non-mpi version of this package, just straight to the mpi builds
export CC=mpicc
export CXX=mpicxx
export FC=mpif90
export F77=mpif77
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
do_build() { 
  cp -al %{name}-%{version} $MPI_COMPILER
  cd $MPI_COMPILER
  make $*
  cd ..
}


# do three builds, one for each mpi stack
%{_openmpi_load}
do_build all
%{_openmpi_unload}

%{_mvapich_load}
do_build osu-mpi1 presta
%{_mvapich_unload}

%{_mvapich2_load}
do_build all
%{_mvapich2_unload}

%install
# do three installs, one for each mpi stack
%{_openmpi_load}
mkdir -p %{buildroot}$MPI_BIN
make -C $MPI_COMPILER DESTDIR=%{buildroot} INSTALL_DIR=$MPI_BIN install
%{_openmpi_unload}

%{_mvapich_load}
mkdir -p %{buildroot}$MPI_BIN
make -C $MPI_COMPILER DESTDIR=%{buildroot} INSTALL_DIR=$MPI_BIN install
%{_mvapich_unload}

%{_mvapich2_load}
mkdir -p %{buildroot}$MPI_BIN
make -C $MPI_COMPILER DESTDIR=%{buildroot} INSTALL_DIR=$MPI_BIN install
%{_mvapich2_unload}

%clean
rm -rf %{buildroot}

%files openmpi
%defattr(-, root, root, -)
%{_libdir}/openmpi/bin/*

%files mvapich
%defattr(-, root, root, -)
%{_libdir}/mvapich/bin/*

%files mvapich2
%defattr(-, root, root, -)
%{_libdir}/mvapich2/bin/*

%changelog
* Fri Jan 15 2010 Doug Ledford <dledford@redhat.com> - 3.2-2.el6
- Rebuild using Fedora MPI package guidelines semantics
- Related: bz543948

* Tue Dec 22 2009 Doug Ledford <dledford@redhat.com> - 3.2-1.el5
- Update to latest release and compile against new mpi libs
- Related: bz518218

* Mon Jun 22 2009 Doug Ledford <dledford@redhat.com> - 3.1-3.el5
- Rebuild against libibverbs that isn't missing the proper ppc wmb() macro
- Related: bz506258

* Sun Jun 21 2009 Doug Ledford <dledford@redhat.com> - 3.1-2.el5
- Rebuild against MPIs that were rebuilt against non-XRC libibverbs
- Related: bz506258

* Thu Apr 23 2009 Doug Ledford <dledford@redhat.com> - 3.1-1
- Upgrade to version from ofed 1.4.1-rc3
- Related: bz459652

* Thu Sep 18 2008 Doug Ledford <dledford@redhat.com> - 3.0-2
- Add no-strict-aliasing compile flag to silence warnings

* Thu Sep 18 2008 Doug Ledford <dledford@redhat.com> - 3.0-1
- Update to latest upstream version
- Compile three times against the three mpi stacks and make three packages
- Resolves: bz451474

* Mon Jan 22 2007 Doug Ledford <dledford@redhat.com> - 2.0-2
- Recreate lost spec file and patches from memory
- Add dist tag to release
- Turn off FORTIFY_SOURCE when building

