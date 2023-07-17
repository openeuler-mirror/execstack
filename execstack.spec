%global commit 4c79120bcdbde0616f592458ccde7035e92ca3d8
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           execstack
Version:        0.5.0
Release:        19
Summary:        Utility to set/clear/query executable stack bit
URL:		    https://github.com/keszybz/prelink
License:        GPLv2+

Source0:        https://github.com/keszybz/prelink/archive/%{commit}.tar.gz#/prelink-%{shortcommit}.tar.gz

Patch0:         Add-PL_ARCH-for-AArch64.patch
Patch1:         coverity.patch
Patch2:         0001-add-riscv-support.patch

BuildRequires:  elfutils-libelf-devel
BuildRequires:  libselinux-devel, libselinux-utils
BuildRequires:  gcc-c++
Requires:       glibc >= 2.2.4-18, coreutils, findutils
Requires:       util-linux, gawk, grep

Obsoletes:      prelink < 0.5.0-8

%description
This package is built from prelink sources but contains just the
execstack binary. It can be used manipulate ELF binaries to run
with or without executable stack.

%prep
%autosetup -n prelink-%{commit} -p1

%build
sed -i -e '/^prelink_LDADD/s/$/ -lpthread/' src/Makefile.{am,in}
%configure
make %{?_smp_mflags} -C gelf
make %{?_smp_mflags} -C gelfx
make %{?_smp_mflags} -C gelfx32
make %{?_smp_mflags} -C src execstack

%check
cp src/execstack test
src/execstack -q test | grep '^-'
src/execstack -s test
src/execstack -q test | grep '^X'
src/execstack -c test
src/execstack -q test | grep '^-'

%install
install -D src/execstack %{buildroot}%{_bindir}/execstack
install -Dm0644 doc/execstack.8 %{buildroot}%{_mandir}/man8/execstack.8

%files
%license COPYING
%doc ChangeLog NEWS README TODO THANKS
%{_bindir}/execstack
%{_mandir}/man8/execstack.8.*

%changelog
* Mon Jul 17 2023 zhangxiang <zhangxiang@iscas.ac.cn> - 0.5.0-19
- add riscv64 support

* Wed Mar 30 2022 jiangxinyu <jiangxinyu@kylinos.cn> - 0.5.0-18
- Add url field

* Fri Feb 11 2022 jiangxinyu <jiangxinyu@kylinos.cn> - 0.5.0-17
- Add BuildRequires: gcc-c++ solves build error

* Fri Jul 30 2021 chenyanpanHW <chenyanpan@huawei.com> - 0.5.0-16
- DESC: delete -Sgit from %autosetup, and delete BuildRequires git

* Fri Oct 30 2020 jiangxinyu <jiangxinyu@kylinos.cn> - 0.5.0-15
- Init execstack project
