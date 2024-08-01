from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
import datetime

from microskel.db_module import Base


class Event(Base):
    __tablename__ = "event"
    id = Column(Integer, primary_key=True)
    city = Column(String(128))
    date = Column(Date)
    name = Column(String(256))
    description = Column(Text)

    def to_dict(self):
        d = {}
        for k in self.__dict__.keys():
            if "_state" not in k:
                d[k] = self.__dict__[k] if "date" not in k else str(self.__dict__[k])
        return d


def configure_views(app):
    @app.route("/events", methods=["GET"])
    def events(db: SQLAlchemy):
        city = request.args.get("city")
        date = request.args.get("date")
        events = db.session.query(Event)
        if city:
            events = events.filter(Event.city == city)
        if date:
            events = events.filter(Event.date == date)
        return [e.to_dict() for e in events.all()], 200

    @app.route("/events", methods=["POST"])
    def create(db: SQLAlchemy):
        city = request.form.get("city", "Brasov")
        name = request.form.get("name")
        description = request.form.get("description")
        date = request.form.get("date")
        date = datetime.date(*[int(s) for s in date.split("-")]) if date else None
        event = Event(city=city, name=name, description=description, date=date)
        db.session.add(event)
        db.session.commit()
        return str(event.id), 201

