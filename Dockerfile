FROM daocloud.io/python:3-onbuild
MAINTAINER ryan.liu <liuhuan086@gmail.com>

RUN mkdir /code
COPY . /code
WORKDIR /code
ENV PYTHONPATH /code
ENV PYTHONUNBUFFERED 0
RUN pip install --trusted-host mirrors.aliyun.com -r requirements.txt
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo 'Asia/Shanghai' >/etc/timezone

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]