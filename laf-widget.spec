
#TODO: provide javadoc after/if upstream fixes the win specific build

Name:           laf-widget
Version:        3.3
Release:        %mkrel 0.0.1
Summary:        Support and base set of additional behaviour and widgets in java look-and-feels
License:        BSD
Group:          Development/Java
Url:            https://laf-widget.dev.java.net/
Source0:        https://laf-widget.dev.java.net/files/documents/5097/77279/laf-widget-all.zip
Source1:        build.xml
BuildRequires:  jpackage-utils
BuildRequires:  java-rpmbuild 
BuildRequires:  ant
BuildRequires:  asm2
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This project contains a collection of "behavioural traits" or "widgets" for third-party Swing look-and-feels. The list of currently provided widgets: 
* Auto-completion (model-based / free-text) on editable combo boxes. 
* Hover preview of minimized internal frames on desktop icons. 
* Menu search panel on menu bars. 
* Hover preview of tab in tabbed panes. 
* Overview dialog on tabbed panes with optional periodic refresh. 
* Tab paging on tabbed panes. 
* Password strength checker on password fields. 
* Lock border on non-editable text components and model-based editable combo boxes. 
* Select all text in text component on focus gain. 
* Context menu on text components with edit actions (copy / paste / cut / delete / select all). 
* Enhanced drag-and-drop support for trees. 
* Scroll pane selector. 
* Selecting / deselecting in text components on Escape key press.

#%package        javadoc
#Summary:        Javadoc for %{name}
#Group:          Development/Java
#
#%description javadoc
#Javadoc for %{name}.

%prep
%setup -q -c %{name}-%{version}
cp %{SOURCE1} build.xml
%remove_java_binaries

%build
ln -s $(build-classpath asm2/asm2) lib/asm-all-2.2.2.jar
%{ant} all

%install
rm -rf %{buildroot}
install -m644 drop/laf-widget.jar -D %{buildroot}%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

#install -d %{buildroot}%{_javadocdir}/%{name}-%{version}
#cp -r docs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
#ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar

#%files javadoc
#%defattr(644,root,root,755)
#%{_javadocdir}/%{name}
#%{_javadocdir}/%{name}-%{version}
  
