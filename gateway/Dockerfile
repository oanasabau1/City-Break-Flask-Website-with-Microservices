FROM microskel

ADD . /gateway
WORKDIR /gateway

RUN pip install -r requirements.txt

CMD ["python", "gateway_service.py"]