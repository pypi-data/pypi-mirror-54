## opsAgent

[![python](https://img.shields.io/badge/python-3.x-blue)]()

> 运维管理后台-监控客户端

## Getting started
```shell
# install dependency package
yum -y install epel-release python36 python36-devel python36-pip libcurl-devel gcc-c++ gcc libgcc

# export PYCURL_SSL_LIBRARY
echo 'export PYCURL_SSL_LIBRARY=nss' >> /root/.bash_profile
source /root/.bash_profile

# install opsAgent
pip3 install opsAgent
```

## Use docker
```shell
docker run -d --name opsAgent -v `pwd`/config.json:/data/config.json fanghongbo/ops-agent:v0.0.3
```
