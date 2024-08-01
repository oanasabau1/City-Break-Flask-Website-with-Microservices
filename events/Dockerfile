FROM microskel

ADD . /events
WORKDIR /events

RUN pip install -r requirements.txt

CMD ["python", "events_service.py"]