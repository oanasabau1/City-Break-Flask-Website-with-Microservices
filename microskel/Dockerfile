FROM python

ADD . /microskel
WORKDIR /microskel

RUN pip install -r requirements.txt
RUN pip install setuptools
RUN pip install wheel

RUN python 2-setup.py sdist bdist_wheel
RUN pip install dist/*.whl

ENV MICROSERVICE_NAME=microservice-base
ENV MICROSERVICE_HOST=localhost
ENV MICROSERVICE_PORT=5000
ENV MICROSERVICE_DEBUG=True

ENV CONSUL_CHECK_INTERVAL=20s
ENV CONSUL_CHECK_TIMEOUT=10s
ENV CONSUL_HOST=localhost
ENV CONSUL_PORT=8500

ENV USE_DB=False
ENV MICROSERVICE_DB_URI=mysql://

ENV LOGSTASH_AGENT_HOST=localhost
ENV LOGSTASH_AGENT_PORT=5959
ENV LOGSTASH_ENABLED=True
