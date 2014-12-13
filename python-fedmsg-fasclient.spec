%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2:        %global __python2 /usr/bin/python2}
%{!?python2_sitelib:  %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%global modname fedmsg_fasclient

Name:               python-fedmsg-fasclient
Version:            0.7
Release:            1%{?dist}
Summary:            A fedmsg consumer that runs fasClient in response to FAS messages

Group:              Development/Libraries
License:            LGPLv2+
URL:                http://pypi.python.org/pypi/fedmsg_fas_client
Source0:            http://pypi.python.org/packages/source/f/%{modname}/%{modname}-%{version}.tar.gz

BuildArch:          noarch

BuildRequires:      python2-devel
BuildRequires:      python-setuptools
BuildRequires:      fedmsg

Requires:           fedmsg
Requires:           fedmsg-hub

%description
A simple script monitoring fedmsg for FAS messages, delaying action
for a few seconds to accumulate messages and avoid pile-up and run fasClient via
ansible.

%prep
%setup -q -n %{modname}-%{version}

# Remove bundled egg-info in case it exists
rm -rf %{modname}.egg-info

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/fedmsg.d/
cp -p fedmsg.d/fasclient-example-config.py \
    %{buildroot}%{_sysconfdir}/fedmsg.d/fasclient.py

%files
%doc README.rst LICENSE
%{python2_sitelib}/%{modname}.py*
%{python2_sitelib}/%{modname}-%{version}*

%config(noreplace) %{_sysconfdir}/fedmsg.d/fasclient.py*

%changelog
* Sat Dec 13 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.7-1
- Update to 0.7
- Also trigger on fas.role.update

* Tue Aug 19 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.6-1
- Update to 0.6
- Do no try to remote the moksha envelop twice

* Tue Aug 19 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.5-1
- Update to 0.5
- Strip the Moksha envelop surrounding the message

* Tue Aug 19 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.4-1
- Update to 0.4
- Better handling of wrongly formatted messages and more reliable logic to check
  if the message is suitable to trigger a fasClient run

* Sun Aug 10 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.3-1
- Update to 0.3
- Let fedmsg-fasclient rely directly on ansible-playbook rather than
  rbac-playbook
- Fix changelog entry for 0.2

* Sat Aug 09 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.2-1
- Update to 0.2
- Fix parsing the fedmsg message by being over-cautious

* Sat Aug 09 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.1.1-1
- Bugfix release fixing how the fields changed are lookedup when a user changes
  his/her account

* Sat Aug 09 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.1-2
- Add missing requires on fedmsg-hub

* Fri Aug 08 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.1-1
- Original work on packaging for Fedora and EPEL
