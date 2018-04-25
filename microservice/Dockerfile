FROM ogc/eoephackaton:latest

USER root
RUN INSTALL_PKGS="rh-python35 rh-python35-python-devel rh-python35-python-setuptools rh-python35-python-pip nss_wrapper \
        httpd24 httpd24-httpd-devel httpd24-mod_ssl httpd24-mod_auth_kerb httpd24-mod_ldap \
        httpd24-mod_session atlas-devel libffi-devel libtool-ltdl enchant" && \
    yum install -y centos-release-scl && \
    yum -y --setopt=tsflags=nodocs install --enablerepo=centosplus $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    # Remove centos-logos (httpd dependency) to keep image size smaller.
    rpm -e --nodeps centos-logos && \
    yum -y clean all --enablerepo='*'


ADD fire_wps.py /usr/bin/local/fire_wps.py
ADD requirements.txt /tmp/requirements.txt
RUN yum -y install gcc libxml2-devel libxslt-devel && yum -y clean all --enablerepo='*'
RUN source scl_source enable rh-python35 && pip install --index-url https://artifactory.vgt.vito.be/api/pypi/python-packages/simple -r /tmp/requirements.txt
USER ogc
CMD source scl_source enable rh-python35 && python /usr/bin/local/fire_wps.py
