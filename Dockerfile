FROM centos

RUN yum -y install sudo git make
RUN yum -y --enablerepo=extras install epel-release
RUN yum -y install python-pip
RUN yum -y install R
RUN yum -y install openssl wget
RUN mkdir -p /repos/Rlibs
RUN wget https://cran.r-project.org/src/contrib/derivmkts_0.2.2.tar.gz
RUN wget https://cran.rstudio.com/src/contrib/mnormt_1.5-5.tar.gz
RUN R CMD INSTALL --library=/repos/Rlibs mnormt_1.5-5.tar.gz derivmkts_0.2.2.tar.gz
RUN pip install setuptools
RUN \
    cd /repos && \
    git clone --depth=1 https://github.com/xhd0216/straddle.git && \
    cd straddle && \
    sudo python setup.py install && \
    pip install virtualenv && \
    make test && \ 
		Rscript 
		
