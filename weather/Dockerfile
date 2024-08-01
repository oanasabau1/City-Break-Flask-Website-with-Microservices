FROM microskel

ENV REDIS_HOST=redis-weather

ADD . /weather
WORKDIR /weather

RUN pip install -r requirements.txt

CMD ["python", "weather_service.py"]