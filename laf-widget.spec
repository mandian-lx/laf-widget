%{?_javapackages_macros:%_javapackages_macros}
%global debug_package %{nil}

Summary:	Support for and base set of additional behaviour and widgets in look-and-feels
Name:		laf-widget
Version:	4.3final
Release:	1
License:	BSD and ASL 2.0 and CC-BY-SA
Group:		Development/Java
URL:		https://java.net/projects/laf-widget
# svn checkout https://svn.java.net/svn/laf-widget~svn/tags/release_4_3_larkspur laf-widget-code
# cp -far laf-widget-code laf-widget-4.3final
# find laf-widget-4.3final -name \.svn -type d -exec rm -fr ./{} \; 2> /dev/null
# tar Jcf laf-widget-4.3final.tar.xz laf-widget-4.3final
Source0:	%{name}-%{version}.tar.xz
Source1:	http://central.maven.org/maven2/net/java/dev/laf-widget/laf-widget/5.0/laf-widget-5.0.pom
Patch0:		%{name}-4.3final-build_xml.patch
Patch1:		%{name}-4.3final-boolean.patch

BuildRequires:	maven-local
BuildRequires:	mvn(asm:asm-all)
BuildRequires:	mvn(org.apache.ant:ant)
BuildRequires:	mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:	mvn(org.pushing-pixels:trident)

%description
Laf-Widget contains a collection of "behavioural traits" or "widgets" for
third-party Swing look-and-feels. The list of currently provided widgets:

  * Auto-completion (model-based / free-text) on editable combo boxes.
  * Hover preview of minimized internal frames on desktop icons.
  * Menu search panel on menu bars.
  * Hover preview of tab in tabbed panes.
  * Overview dialog on tabbed panes with optional periodic refresh.
  * Tab paging on tabbed panes.
  * Password strength checker on password fields.
  * Lock border on non-editable text components and model-based editable combo
    boxes.
  * Select all text in text component on focus gain.
  * Context menu on text components with edit actions (copy / paste / cut
    / delete / select all).
  * Enhanced drag-and-drop support for trees.
  * Scroll pane selector.
  * Selecting / deselecting in text components on Escape key press.

%files -f .mfiles
%doc src/org/jvnet/lafwidget/ASM.license
%doc src/org/jvnet/lafwidget/BlogOfBug.license
%doc src/org/jvnet/lafwidget/JiBX.license
%doc src/org/jvnet/lafwidget/LafWidget.license
%doc src/org/jvnet/lafwidget/Looks.license
%doc src/org/jvnet/lafwidget/TangoIcons.license

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{name}
BuildArch:	noarch

%description javadoc
API documentation for %{name}.

%files javadoc -f .mfiles-javadoc
#%docdir www

#----------------------------------------------------------------------------

%prep
%setup -q
# Delete all prebuild JARs and classes
find . -name "*.jar" -delete
find . -name "*.class" -delete

# Apply all patches
%patch0 -p1 -b .orig
%patch1 -p1 -b .bool

# pom.xml
cp %{SOURCE1} ./pom.xml

# Fix version
%pom_xpath_replace "pom:project/pom:version" "<version>%{version}</version>" .

# Fix dependency
sed -i -e 's|<groupId>ant</groupId>|<groupId>org.apache.ant</groupId>|g' ./pom.xml

# Set the sources and tests directory
%pom_xpath_inject "pom:project/pom:build" "
	<sourceDirectory>src/</sourceDirectory>
	<testSourceDirectory>src/test</testSourceDirectory>"

# compiler plugin
%pom_xpath_inject "pom:plugin[pom:artifactId[./text()='maven-compiler-plugin']]/pom:configuration" "
<includes>
	<include>org/**/*.java</include>
	<include>contrib/**/*.java</include>
</includes>
<excludes>
	<exclude>contrib/com/blogofbug/examples/*</exclude>
</excludes>"

# javadoc plugin
%pom_add_plugin :maven-javadoc-plugin . "
<configuration>
	<excludePackageNames>contrib:test</excludePackageNames>
</configuration>"

# resources
%pom_xpath_inject "pom:build" "
<resources>
	<resource>
		<directory>src</directory>
		<excludes>
			<exclude>**/*.java</exclude>
			<exclude>contrib/</exclude>
			<exclude>test/</exclude>
		</excludes>
		<includes>
			<include>**/*.license</include>
			<include>**/*.properties</include>
			<include>**/*.png</include>
		</includes>
	</resource>
</resources>" .

# Bundle
%pom_xpath_replace "pom:project/pom:packaging" "<packaging>bundle</packaging>" .

# Add an OSGi compilant MANIFEST.MF
%pom_add_plugin org.apache.felix:maven-bundle-plugin . "
<extensions>true</extensions>
<configuration>
	<supportedProjectTypes>
		<supportedProjectType>bundle</supportedProjectType>
		<supportedProjectType>jar</supportedProjectType>
	</supportedProjectTypes>
	<instructions>
	        <!-- FIXME: find a way to use option org.osgi.framework.system.packages.extra -->
		<Import-Package>
			com.sun.java.swing.plaf.windows*;resolution:=optional,
			org.apache.tools.ant*;resolution:=optional,
			org.objectweb.asm*;resolution:=optional,
			*
		</Import-Package>
		<Bundle-Name>\${project.artifactId}</Bundle-Name>
		<Bundle-Version>\${project.version}</Bundle-Version>
	</instructions>
</configuration>
<executions>
	<execution>
		<id>bundle-manifest</id>
		<phase>process-classes</phase>
		<goals>
			<goal>manifest</goal>
		</goals>
	</execution>
</executions>"

# Add the META-INF/INDEX.LIST (fix jar-not-indexed warning) and
# the META-INF/MANIFEST.MF to the jar archive
%pom_add_plugin :maven-jar-plugin . "
<executions>
	<execution>
		<phase>package</phase>
		<configuration>
			<archive>
				<manifestFile>\${project.build.outputDirectory}/META-INF/MANIFEST.MF</manifestFile>
				<manifest>
					<addDefaultImplementationEntries>true</addDefaultImplementationEntries>
					<addDefaultSpecificationEntries>true</addDefaultSpecificationEntries>
				</manifest>
				<index>true</index>
			</archive>
		</configuration>
		<goals>
			<goal>jar</goal>
		</goals>
	</execution>
</executions>"

%build
%mvn_build -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

