FROM microskel

ADD . /service_two
WORKDIR /service_two

RUN pip install -r requirements.txt

CMD ["python", "service_two.py"]
