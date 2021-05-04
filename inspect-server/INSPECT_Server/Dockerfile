# 基于的基础镜像
FROM python:3.7

# 维护者信息
MAINTAINER LHM  lhm@ikahe.com

# 添加阿里云pip
COPY ./TCP/pip.conf /root/.pip/pip.conf

# 代码添加到code文件夹
ADD ./TCP /code

# 设置code文件夹是工作目录
WORKDIR /code

# 更新pip版本
RUN /usr/local/bin/python -m pip install --upgrade pip


# 安装支持
RUN pip install -r requirements.txt

CMD ["python", "/code/main.py"]