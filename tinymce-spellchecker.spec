%define		ver %(echo %{version} | tr . _)
Summary:	TinyMCE spellchecker plugin
Name:		tinymce-spellchecker
Version:	2.0.2
Release:	0.1
License:	LGPL v2
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/tinymce/tinymce_spellchecker_php_%{ver}.zip
# Source0-md5:	71ea3f554466fed09530a89fb98e6eee
URL:		http://tinymce.moxiecode.com/
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
Serverside spellchecker plugin, current version only supports PHP with
pspell or the Google XML service.

%prep
%setup -qc
mv spellchecker/* .
cat <<'EOF' > apache.conf
Alias /%{_webapp} %{_appdir}/htdocs
<Directory %{_appdir}/htdocs>
	Allow from all
</Directory>
EOF

cat > lighttpd.conf <<'EOF'
alias.url += (
    "/%{_webapp}" => "%{_appdir}/htdocs",
)
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/htdocs}

cp -a editor_plugin.js rpc.php css img $RPM_BUILD_ROOT%{_appdir}/htdocs
cp -a classes includes $RPM_BUILD_ROOT%{_appdir}
cp -a config.php $RPM_BUILD_ROOT%{_sysconfdir}
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -a lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc changelog
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%{_appdir}