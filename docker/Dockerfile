FROM centos

RUN yum -y install sudo git make
RUN yum -y --enablerepo=extras install epel-release
RUN yum -y install python-pip
RUN yum -y install R
RUN yum -y install openssl wget echo libcurl-devel
RUN echo "r <- getOption('repos'); r['CRAN'] <- 'http://cran.us.r-project.org'; options(repos = r);" > ~/.Rprofile
RUN mkdir -p /repos/Rlibs
RUN Rscript -e "install.packages('derivmkts')"
RUN Rscript -e "install.packages('tseries')"
RUN pip install setuptools
RUN yum install -y MySQL-python
ADD https://api.github.com/repos/xhd0216/straddle/git/refs/heads version.json
RUN \
    cd /repos && \
    git clone --depth=1 https://github.com/xhd0216/straddle.git && \
    cd straddle && \
    sudo python setup.py install
RUN yum -y install crontabs

RUN sed -i -e '/pam_loginuid.so/s/^/#/' /etc/pam.d/crond
ADD cron.txt /etc/cron.d/cron_test
RUN chmod 644 /etc/cron.d/cron_test

RUN crontab /etc/cron.d/cron_test

CMD crond && tail -f /dev/null

RUN mv /etc/localtime /etc/localtime.bk
RUN ln -s /usr/share/zoneinfo/America/Los_Angeles /etc/localtime
