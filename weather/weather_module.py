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
            return 'No data found for the specified key', 404

        try:
            weather = weather.decode('utf-8')
            weather = json.loads(weather)
        except json.JSONDecodeError:
            return 'Data format error', 500

        print(f'weather = {weather}')
        return json.dumps(weather), 200

    @app.route("/weather", methods=["POST"])
    def post():
        keys = ('temperature', 'humidity', 'wind')
        weather = {k: request.form.get(k) for k in keys}
        city = request.form.get('city', 'Brasov')
        date = request.form.get('date', str(datetime.date.today()))
        key = f'{city}-{date}' if date else city
        try:
            client.set(key, json.dumps(weather))
        except Exception as e:
            print(f'Failed to set data in Redis: {e}')
            return 'Internal server error', 500

        return 'OK', 200

