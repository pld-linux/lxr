Summary:	Linux Cross-Reference
Name:		lxr
Version:	0.9.10
Release:	2
License:	GPL
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/lxr/%{name}-%{version}.tgz
# Source0-md5:	c6e7716a96f1ca9e151b02d5de423c66
Source1:	%{name}-apache.conf
Source2:	%{name}-httpd.conf
Patch0:		%{name}-conf.patch
Patch1:		%{name}-INC.patch
URL:		http://sourceforge.net/projects/lxr
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	ctags
#Requires:	perl-DBD-Pg
#Requires:	perl-DBD-mysql
Requires:	perl-DBI
Requires:	perl-File-MMagic
#Requires:	rcs
Requires:	swish-e >= 2.1
Requires:	webapps
Suggests:	perl-Linux-KernelSort
Conflicts:	apache-base < 2.4.0-1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	perl(NDBM_File)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_lxrdir		%{_datadir}/%{_webapp}

%description
The Linux Cross-Reference project is the testbed application of a
general hypertext cross-referencing tool. (Or the other way around.)

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
for f in apache2-require.pl diff genxref ident search source templates/lxr.conf ; do
	sed -i -e 's|@@LXRDIR@@|%{_lxrdir}|' \
	       -e 's|@@PERLVENDOR@@|%{perl_vendorlib}|g' $f
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{perl_vendorlib},%{_lxrdir},/var/lib/%{_webapp}/{swish,glimpse}}

install -p templates/lxr.conf $RPM_BUILD_ROOT%{_sysconfdir}/lxr.conf
ln -s %{_sysconfdir}/lxr.conf $RPM_BUILD_ROOT%{_lxrdir}/

install -p swish-e.conf $RPM_BUILD_ROOT%{_sysconfdir}/
ln -s %{_sysconfdir}/swish-e.conf $RPM_BUILD_ROOT%{_lxrdir}/

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

install -p diff genxref ident search source Local.pm LXRversion.pm apache2-require.pl \
	$RPM_BUILD_ROOT%{_lxrdir}/

cp -a lib/LXR $RPM_BUILD_ROOT%{perl_vendorlib}/
cp -a templates/*.{css,html} $RPM_BUILD_ROOT%{_lxrdir}/

%post
%banner %{name} -e <<EOF
###################################################################
#                                                                 #
# NOTICE:                                                         #
# You need one of perl-DBD-mysql, perl-DBD-Pg, perl-DBD-Oracle    #
# depending of which database you want to use.                    #
#                                                                 #
# If you are installing for the first time, You will have to      #
# create the LXR database tables. Look into directory             #
# %{_docdir}/%{name}-%{version}/initdb-*                          #
# to find out how to do this for your database.                   #
#                                                                 #
###################################################################
EOF

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache-base
%webapp_unregister httpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc BUGS CHANGES CREDITS.txt ChangeLog HACKING INSTALL RELEASING initdb-* robots.txt
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lxr.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/swish-e.conf

%dir %{_lxrdir}
%attr(755,root,root) %{_lxrdir}/diff
%attr(755,root,root) %{_lxrdir}/genxref
%attr(755,root,root) %{_lxrdir}/ident
%attr(755,root,root) %{_lxrdir}/search
%attr(755,root,root) %{_lxrdir}/source
%{_lxrdir}/apache2-require.pl
%{_lxrdir}/*.html
%{_lxrdir}/*.css
%{_lxrdir}/*.conf
%{_lxrdir}/*.pm
%{perl_vendorlib}/LXR
%dir /var/lib/%{_webapp}
%dir /var/lib/%{_webapp}/glimpse
%dir /var/lib/%{_webapp}/swish
