FROM python:3.9.16-slim-buster
VOLUME /tmp

WORKDIR  /opt/app-cloud/app
ENV LC_ALL=en_US.UTF-8
ENV CD_SERVER_LOG_DIR=/var/log/cd/cd
EXPOSE 8080
RUN mkdir -p /var/log/cd/cd && mkdir -p /usr/jmx_prometheus

COPY requirements.txt /opt/app-cloud/app/
# RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 config --user set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 config --user set global.trusted-host pypi.tuna.tsinghua.edu.cn
RUN pip3 install -r requirements.txt --trusted-host pypi.tuna.tsinghua.edu.cn

COPY . /opt/app-cloud/app

ENTRYPOINT ["python3", "server.py"]