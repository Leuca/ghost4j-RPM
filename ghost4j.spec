Name:			ghost4j
Version:		1.0.5
Release:		%autorelease
Summary:		Java wrapper for Ghostscript C API + PS/PDF document handling API 
License:		LGPL 3.0
URL:			http://www.ghost4j.org/
BuildArch:		noarch
ExclusiveArch:	%{java_arches} noarch

Source0:		https://github.com/zippy1978/ghost4j/archive/%{version}/%{name}-%{version}.tar.gz

# Support OpenPDF 3.0.0
Patch0:		ghost4j-support-openpdf-3.0.0.patch

%if 0%{?fedora} >= 40 || 0%{?rhel} >= 10
BuildRequires:  maven-local
%else
BuildRequires:  maven-local-openjdk11
%endif
BuildRequires:	ghostscript
BuildRequires:	mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:	mvn(junit:junit)
BuildRequires:	mvn(log4j:log4j)
BuildRequires:	mvn(commons-beanutils:commons-beanutils)
BuildRequires:	mvn(com.github.librepdf:openpdf)
BuildRequires:	mvn(net.java.dev.jna:jna)
BuildRequires:	mvn(org.apache.xmlgraphics:xmlgraphics-commons)

Requires:		ghostscript

%description
Ghost4J binds the Ghostscript C API to bring Ghostscript power to the Java world. It also provides a high-level API to handle PDF and Postscript documents with objects.

%{?javadoc_package}

%prep
%autosetup -p1

# Swap itext with openpdf
%pom_remove_dep com.lowagie:itext
%pom_add_dep com.github.librepdf:openpdf

%pom_xpath_remove "pom:build/pom:extensions"
%pom_remove_plugin org.apache.maven.plugins:maven-javadoc-plugin

# Fix compatibility with jna 5.0.0+
sed -i 's/import com.sun.jna.Pointer;/import com.sun.jna.Pointer;\nimport com.sun.jna.Native;/' src/main/java/org/ghost4j/Ghostscript.java
sed -i 's/Pointer.SIZE/Native.POINTER_SIZE/' src/main/java/org/ghost4j/Ghostscript.java
sed -i 's/?/String/' src/main/java/org/ghost4j/GhostscriptLibrary.java
sed -i 's/win32.StdCallLibrary.StdCallCallback/Callback/' src/main/java/org/ghost4j/GhostscriptLibrary.java
sed -i 's/StdCallCallback/Callback/' src/main/java/org/ghost4j/GhostscriptLibrary.java

%pom_xpath_set //pom:source 1.8
%pom_xpath_set //pom:target 1.8

%build
# Test are broken
# ...it would be nice to fix them
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%license LICENSE
%doc README.md

%changelog
%autochangelog
