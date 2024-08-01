from flask import request

import json
import os
import datetime
import redis

client = redis.Redis(host=os.environ.get('REDIS_HOST', 'redis'))


def configure_views(app):
    @app.route("/weather", methods=["GET"])
    def get():
        city = request.args.get("city")
        date = request.args.get("date", str(datetime.date.today()))
        key = f'{city}-{date}' if date else city
        weather = client.get(key)
        print(f'key={key}')
        if not weather:
            return 'No data', 401
        print(f'weather = {weather}')
        weather = client.get(key)
        weather = json.loads(weather)
        return json.dumps(weather), 200

    @app.route("/weather", methods=["POST"])
    def post():
        keys = ('temperature', 'humidity', 'wind')
        weather = {k: request.form.get(k) for k in keys}
        city = request.form.get('city', 'Brasov')
        date = request.form.get('date', str(datetime.date.today()))
        key = f'{city}-{date}' if date else city
        client.set(key, json.dumps(weather))
        return 'OK', 200
