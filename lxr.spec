%include	/usr/lib/rpm/macros.perl
Summary:	Linux Cross-Reference
Name:		lxr
Version:	0.9.9
Release:	0.1
License:	GPL
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/lxr/%{name}-%{version}.tgz
# Source0-md5:	0424855d7f9c13ff080e4e1cca99273a
Source1:	%{name}-apache.conf
Source2:	%{name}-httpd.conf
Patch1:		%{name}-conf.patch
Patch3:		%{name}-INC.patch
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
#%patch1 -p1
%patch3 -p1
for f in diff find genxref ident search source templates/lxr.conf ; do
	sed -i -e 's|@@LXRDIR@@|%{_lxrdir}|' \
	       -e 's|@@PERLVENDOR@@|%{perl_vendorlib}|g' $f
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{perl_vendorlib},%{_lxrdir},/var/lib/%{_webapp}/{swish,glimpse}}

install templates/lxr.conf $RPM_BUILD_ROOT%{_sysconfdir}/lxr.conf
ln -s %{_sysconfdir}/lxr.conf $RPM_BUILD_ROOT%{_lxrdir}/

install swish-e.conf $RPM_BUILD_ROOT%{_sysconfdir}/
ln -s %{_sysconfdir}/swish-e.conf $RPM_BUILD_ROOT%{_lxrdir}/

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

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
