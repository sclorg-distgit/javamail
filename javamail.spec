%{?scl:%scl_package javamail}
%{!?scl:%global pkg_name %{name}}

%{?thermostat_find_provides_and_requires}

Name:           %{?scl_prefix}javamail
Version:        1.4.6
Release:        7.3%{?dist}
Summary:        Java Mail API
License:        CDDL or GPLv2 with exceptions
URL:            http://www.oracle.com/technetwork/java/javamail
BuildArch:      noarch

# ./create-tarball.sh
Source0:        javamail-1.4.6-clean.tar.gz
Source1:        create-tarball.sh

BuildRequires:  maven-local
BuildRequires:  jvnet-parent
BuildRequires:  maven-assembly-plugin
BuildRequires:  maven-dependency-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-plugin-bundle
BuildRequires:  maven-plugin-build-helper

# Adapted from the classpathx-mail (and JPackage glassfish-javamail) Provides.
Provides:       %{?scl_prefix}javamail-monolithic = %{version}-%{release}

%description
The JavaMail API provides a platform-independent and protocol-independent
framework to build mail and messaging applications.


%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
%{summary}.


%prep
%{?scl:scl enable %{scl} - << "EOF"}
%setup -q -n %{pkg_name}-%{version}

# Remove profiles containing demos and other stuff that is not
# supposed to be deployable.
%pom_xpath_remove /pom:project/pom:profiles

# Upstream uses maven-dependency-plugin for downloading and unpacking binary JARs
# instead of specifying proper dependencies between modules
%pom_xpath_inject "pom:project" "<dependencies></dependencies>" mailapi
%pom_add_dep 'com.sun.mail:javax.mail:${mail.version}' mailapi

%pom_xpath_inject "pom:project" "<dependencies></dependencies>" mailapijar
%pom_add_dep 'com.sun.mail:javax.mail:${mail.version}' mailapijar

%pom_xpath_inject "pom:project" "<dependencies></dependencies>" parent-distrib
%pom_add_dep 'com.sun.mail:javax.mail:${mail.version}' parent-distrib

# Install parent POM
%pom_xpath_inject pom:project/pom:modules "<module>parent-distrib</module>"

# osgiversion-maven-plugin is used to set ${mail.osgiversion} property
# based on ${project.version}. We don't have osgiversion plugin in
# Fedora so we'll set ${mail.osgiversion} explicitly.
%pom_remove_plugin org.glassfish.hk2:osgiversion-maven-plugin
%pom_xpath_inject /pom:project/pom:properties "<mail.osgiversion>%{version}</mail.osgiversion>"

# Alternative names for super JAR containing API and implementation.
%mvn_alias javax.mail:javax.mail-api javax.mail:mailapi \
           org.eclipse.jetty.orbit:javax.mail.glassfish
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - << "EOF"}
%mvn_build -f
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc mail/src/main/java/overview.html
%doc mail/src/main/resources/META-INF/LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc mail/src/main/resources/META-INF/LICENSE.txt

%changelog
* Tue Jan 21 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4.6-7.3
- Rebuild to fix provides/requires

* Mon Nov 18 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4.6-7.2
- Fix provides
- Disable tests for now

* Mon Nov 18 2013 Michal Srb <msrb@redhat.com> - 1.4.6-7.1
- Enable SCL for thermostat

* Fri Aug 02 2013 Michal Srb <msrb@redhat.com> - 1.4.6-7
- Add create-tarball.sh script to SRPM

* Fri Aug 02 2013 Michal Srb <msrb@redhat.com> - 1.4.6-6
- Add create-tarball.sh script to SRPM

* Fri Jul 26 2013 Michal Srb <msrb@redhat.com> - 1.4.6-5
- Clean up tarball

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.6-4
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Mon Jun 24 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.6-3
- Resore Maven aliases to point to super JAR

* Wed Jun 12 2013 Michal Srb <msrb@redhat.com> - 1.4.6-2
- Fix FTBFS (Resolves: #973560)

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
