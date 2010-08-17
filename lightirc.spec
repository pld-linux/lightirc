Summary:	Flash IRC Chat
Name:		lightirc
Version:	0.9.9.3
Release:	1
License:	free (but not open)
Group:		Applications/WWW
Source0:	http://www.lightirc.com/release/lightIRC_%{version}.zip
# Source0-md5:	5d67f5d2aab9076e685af85b63e39ef7
URL:		http://www.lightirc.com/
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	js-swfobject
Requires:	webapps
Requires:	webserver(alias)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
lightIRC is a free Flash IRC client that includes all well known IRC
features. It supports stylesheets for its own skins, has support for
multiple languages, and can be used with every IRCd.

%prep
%setup -qc

mv lightIRC/*.txt .
rm lightIRC/swfobject.js
%undos lightIRC/*.html

cat > apache.conf <<'EOF'
Alias /%{name}/swfobject.js %{_datadir}/swfobject/swfobject.js
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

cat > lighttpd.conf <<'EOF'
alias.url += (
    "/%{name}/swfobject.js" => "%{_datadir}/swfobject/swfobject.js",
    "/%{name}" => "%{_appdir}",
)
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}
cp -a lightIRC/* $RPM_BUILD_ROOT%{_appdir}

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
%doc readme.txt changelog.txt
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%dir %{_appdir}
%{_appdir}/*.swf
%{_appdir}/styles
%config(noreplace) %verify(not md5 mtime size) %{_appdir}/index.html
