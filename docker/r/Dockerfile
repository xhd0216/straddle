FROM r-base
# this is debian

RUN apt-get update
RUN apt-get install -y aptitude
RUN apt-get install -y libcurl4-openssl-dev
RUN apt-get install -y libxml2-dev

RUN echo "r <- getOption('repos'); r['CRAN'] <- 'http://cran.us.r-project.org'; options(repos = r);" > ~/.Rprofile
RUN mkdir -p /repos/Rlibs
RUN Rscript -e "install.packages('derivmkts')"
RUN Rscript -e "install.packages('tseries')"

RUN apt-get install libmysqlclient-dev
RUN apt-get install python-pip
RUN apt-get install git

ADD https://api.github.com/repos/xhd0216/straddle/git/refs/heads version.json
RUN \
    mkdir /repos && \
    cd /repos && \
    git clone --depth=1 https://github.com/xhd0216/straddle.git && \
    cd straddle && \
    python setup.py install
