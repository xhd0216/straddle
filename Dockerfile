FROM centos

RUN yum -y install sudo git make
RUN yum -y --enablerepo=extras install epel-release
RUN yum -y install python-pip
RUN yum -y install R
RUN yum -y install openssl
RUN mkdir -p /repos
RUN pip install setuptools
RUN \
    cd /repos && \
    git clone https://github.com/xhd0216/straddle.git && \
    cd straddle && \
    sudo python setup.py install && \
    pip install virtualenv && \
    make test

RUN market_watcher_parser
