FROM centos

RUN yum install -y sudo git make
RUN yum -y --enablerepo=extras install epel-release
RUN yum -y install python-pip
RUN mkdir -p /repos
RUN pip install setuptools
RUN \
    cd /repos && \
    git clone https://github.com/xhd0216/straddle.git && \
    cd straddle && \
    sudo python setup.py install && \
    pip install virtualenv && \
    make test
