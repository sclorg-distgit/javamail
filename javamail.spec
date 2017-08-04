%{?scl:%scl_package javamail}
%{!?scl:%global pkg_name %{name}}

Name:           %{?scl_prefix}javamail
Version:        1.5.2
Release:        4.2%{?dist}
Summary:        Java Mail API
License:        CDDL or GPLv2 with exceptions
URL:            http://www.oracle.com/technetwork/java/javamail
BuildArch:      noarch

Source:        https://java.net/projects/javamail/downloads/download/source/javamail-%{version}-src.zip

BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix}mvn(junit:junit)
BuildRequires:  %{?scl_prefix}mvn(net.java:jvnet-parent:pom:)
BuildRequires:  %{?scl_prefix}mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.mojo:build-helper-maven-plugin)

# Adapted from the classpathx-mail (and JPackage glassfish-javamail) Provides.
Provides:       %{?scl_prefix}javamail-monolithic = %{version}-%{release}

Provides:       %{?scl_prefix}javax.mail

%description
The JavaMail API provides a platform-independent and protocol-independent
framework to build mail and messaging applications.

%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
%{summary}.

%prep
%setup -n %{pkg_name}-%{version} -q -c

add_dep() {
    %pom_xpath_inject pom:project "<dependencies/>" ${2}
    %pom_add_dep com.sun.mail:${1}:%{version}:provided ${2}
}

add_dep smtp mailapi
add_dep javax.mail smtp
add_dep javax.mail pop3
add_dep javax.mail imap
add_dep javax.mail mailapijar

# Remove profiles containing demos and other stuff that is not
# supposed to be deployable.
%pom_xpath_remove /pom:project/pom:profiles

# osgiversion-maven-plugin is used to set ${mail.osgiversion} property
# based on ${project.version}. We don't have osgiversion plugin in
# Fedora so we'll set ${mail.osgiversion} explicitly.
%pom_remove_plugin org.glassfish.hk2:osgiversion-maven-plugin
%pom_remove_dep javax.activation:activation
%pom_xpath_inject /pom:project/pom:properties "<mail.osgiversion>%{version}</mail.osgiversion>"
%pom_xpath_inject /pom:project/pom:build/pom:plugins/pom:plugin/pom:configuration/pom:instructions "<_nouses>true</_nouses>"

# Alternative names for super JAR containing API and implementation.
%mvn_alias com.sun.mail:mailapi javax.mail:mailapi
%mvn_alias com.sun.mail:javax.mail javax.mail:mail \
           org.eclipse.jetty.orbit:javax.mail.glassfish
%mvn_file "com.sun.mail:{javax.mail}" %{pkg_name}/@1 %{pkg_name}/mail

%build
# Some tests fail on Koji due to networking limitations
%mvn_build -- -Dmaven.test.failure.ignore=true

%install
%mvn_install

install -d -m 755 %{buildroot}%{_javadir}/javax.mail/
ln -sf ../%{pkg_name}/javax.mail.jar %{buildroot}%{_javadir}/javax.mail/

%files -f .mfiles
%doc mail/src/main/java/overview.html
%doc mail/src/main/resources/META-INF/LICENSE.txt
%{_javadir}/javax.mail/

%files javadoc -f .mfiles-javadoc
%doc mail/src/main/resources/META-INF/LICENSE.txt

%changelog
* Thu Jun 22 2017 Michael Simacek <msimacek@redhat.com> - 1.5.2-4.2
- Mass rebuild 2017-06-22

* Wed Jun 21 2017 Java Maintainers <java-maint@redhat.com> - 1.5.2-4.1
- Automated package import and SCL-ization

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 6 2015 Alexander Kurtakov <akurtako@redhat.com> 1.5.2-1
- Update to upstream 1.5.2 using upstream tarball.

* Fri Mar 6 2015 Alexander Kurtakov <akurtako@redhat.com> 1.5.1-5
- Remove javax.activation:activation dependency.

* Mon Aug  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5.1-4
- Fix build-requires on jvnet-parent

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 31 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5.1-2
- Regenerate build-requires

* Mon Mar 31 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5.1-1
- Update to upstream version 1.5.1

* Mon Mar 31 2014 Alexander Kurtakov <akurtako@redhat.com> 1.5.0-8
- Do not generate uses clauses for osgi -too strict linking.

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5.0-7
- Use Requires: java-headless rebuild (#1067528)

* Mon Aug 12 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5.0-6
- Add forgotten provides

* Mon Aug 12 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5.0-5
- Add javax.mail provides and directory

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5.0-3
- Add compat symlink for javax.mail:mail

* Mon Jun 24 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5.0-2
- Add Maven alias for javax.mail:mail

* Mon Jun 24 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5.0-1
- Update to upstream version 1.5.0

* Thu Mar  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.6-1
- Update to upstream version 1.4.6

* Mon Mar  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.3-16
- Add depmap for org.eclipse.jetty.orbit
- Resolves: rhbz#917624

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.4.3-14
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Oct 11 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.3-13
- Fix URL

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.3-11
- Update OSGi manifest patch

* Tue May 29 2012 Gerard Ryan <galileo@fedoraproject.org> - 1.4.3-10
- Add extra information to OSGi manifest
- Fix rpmlint error about mavendepmapfragdir

* Wed Mar 21 2012 Alexander Kurtakov <akurtako@redhat.com> 1.4.3-9
- Drop tomcat6-jsp-api requires - it's dependency management not dependency, hence not needed.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Alexander Kurtakov <akurtako@redhat.com> 1.4.3-7
- Build with maven3.
- Adapt to current guidelines.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec  8 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4.3-5
- Fix pom filenames (#655806)
- Versionless jars/javadocs (new guidelines)
- Migrate to tomcat6 (#652004)
- Other cleanups

* Wed Sep 8 2010 Alexander Kurtakov <akurtako@redhat.com> 1.4.3-4
- Add surefire provider BR.

* Wed Sep 8 2010 Alexander Kurtakov <akurtako@redhat.com> 1.4.3-3
- Drop gcj_support.
- Use javadoc:aggregate.

* Fri Jan  8 2010 Mary Ellen Foster <mefoster at gmail.com> 1.4.3-2
- Remove unnecessary (build)requirement tomcat5-servlet-2.4-api
- Move jar files into subdirectory

* Wed Dec  2 2009 Mary Ellen Foster <mefoster at gmail.com> 1.4.3-1
- Initial package
