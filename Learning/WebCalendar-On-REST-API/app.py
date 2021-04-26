from flask import Flask
from flask import abort
import sys
from flask_restful import Api, Resource
from flask_restful import inputs
from flask_restful import reqparse
from flask_restful import fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import date


app = Flask(__name__)
#from app import db
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'

# write your code here

event_fields = {
    'id':   fields.Integer,
    'event':    fields.String,
    'date': fields.DateTime(dt_format='iso8601')
}

class EventDb(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)

#from app import db
db.create_all()
api = Api(app)
parser = reqparse.RequestParser()
tparser = reqparse.RequestParser()
parser.add_argument(
    'date',
    type=inputs.date,
    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
    required=True
)
parser.add_argument(
    'event',
    type=str,
    help="The event name is required!",
    required=True
)
tparser.add_argument(
    'start_time',
    type=inputs.date,
    required=False
)
tparser.add_argument(
    'end_time',
    type=inputs.date,
    required=False
)


class EventResource(Resource):
    @marshal_with(event_fields)
    def get(self):
        return EventDb.query.filter(EventDb.date == date.today()).all()

class GetEventById(Resource):
    @marshal_with(event_fields)
    def get(self, eventid):
        event = EventDb.query.filter(EventDb.id == eventid).first()
        if event is None:
            abort(404, "The event doesn't exist!")
        return event

    def delete(self, eventid):
        event = EventDb.query.filter(EventDb.id == eventid).first()
        if event is None:
            abort(404, "The event doesn't exist!")
        db.session.delete(event)
        db.session.commit()
        return {
                    "message": "The event has been deleted!",
               }

class GetEventsByDates(Resource):
    @marshal_with(event_fields)
    def get(self):
        args = tparser.parse_args()
        if args['start_time'] is None or args['end_time'] is None:
            return EventDb.query.all()
        else:
            events = EventDb.query.filter(EventDb.date.between(args['start_time'].date(), args['end_time'].date())).all()
            return events

class EventPost(Resource):
    def post(self):
        args = parser.parse_args()
        event = EventDb(event=args['event'], date=args['date'].date())
        db.session.add(event)
        db.session.commit()
        db.session.remove()
        return {
                    "message": "The event has been added!",
                    "event": args['event'],
                    "date": str(args['date'].date())
               }

    # @marshal_with(event_fields)
    # def get(self):
    #     events = EventDb.query.all()
    #     return events


api.add_resource(EventResource, '/event/today')
api.add_resource(EventPost, '/event')
api.add_resource(GetEventById, '/event/<int:eventid>')
api.add_resource(GetEventsByDates, '/event')


# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
