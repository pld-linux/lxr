%include	/usr/lib/rpm/macros.perl
Summary:	Linux Cross-Reference
Name:		lxr
Version:	0.9.4
Release:	2
License:	GPL
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/lxr/%{name}-%{version}.tgz
# Source0-md5:	15846a8be01a792cfd2f6adfb90b3738
Source1:	%{name}-apache.conf
Source2:	%{name}.htaccess
Patch0:		%{name}-CVS20060222.patch
Patch1:		%{name}-conf.patch
Patch2:		%{name}-mysql5.patch
Patch3:		%{name}-INC.patch
URL:		http://lxr.linux.no/
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	ctags
Requires:	perl-DBI
#Requires:	perl-DBD-mysql
#Requires:	perl-DBD-Pg
Requires:	perl-File-MMagic
#Requires:	rcs
Requires:	swish-e >= 2.1
Requires:	webapps
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	perl(NDBM_File)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_lxrdir		%{_datadir}/%{_webapp}

%description
The Linux Cross-Reference project is the testbed application
of a general hypertext cross-referencing tool.
(Or the other way around.)

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
sed -i -e 's|@@DATADIR@@|%{_lxrdir}|' genxref

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{perl_vendorlib},%{_lxrdir},/var/lib/%{_webapp}/{swish,glimpse}}

sed -e "s|PERLVENDOR|%{perl_vendorlib}|g" templates/lxr.conf > $RPM_BUILD_ROOT%{_sysconfdir}/lxr.conf
ln -s %{_sysconfdir}/lxr.conf $RPM_BUILD_ROOT%{_lxrdir}/

install swish-e.conf $RPM_BUILD_ROOT%{_sysconfdir}/
ln -s %{_sysconfdir}/swish-e.conf $RPM_BUILD_ROOT%{_lxrdir}/

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

install %{SOURCE2} $RPM_BUILD_ROOT%{_lxrdir}/.htaccess

install diff find genxref ident search source Local.pm \
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
###################################################################             
EOF                                                                             

%triggerin -- apache1
%webapp_register apache %{_webapp}

%triggerun -- apache1
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc BUGS CREDITS.txt HACKING INSTALL initdb-* notes
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lxr.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/swish-e.conf

%dir %{_lxrdir}
%{_lxrdir}/.htaccess
%attr(755,root,root) %{_lxrdir}/diff
%attr(755,root,root) %{_lxrdir}/find
%attr(755,root,root) %{_lxrdir}/genxref
%attr(755,root,root) %{_lxrdir}/ident
%attr(755,root,root) %{_lxrdir}/search
%attr(755,root,root) %{_lxrdir}/source
%{_lxrdir}/*.html
%{_lxrdir}/*.css
%{_lxrdir}/*.conf
%{_lxrdir}/*.pm
%{perl_vendorlib}/LXR
%dir /var/lib/%{_webapp}
%dir /var/lib/%{_webapp}/glimpse
%dir /var/lib/%{_webapp}/swish
