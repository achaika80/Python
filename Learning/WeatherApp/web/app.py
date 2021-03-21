from flask import Flask, session
from flask import render_template
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from flask import flash
import sys
import requests
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)
app.secret_key = "12qwe345556"

# write your code here

class city(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<City %r>' % self.name


db.create_all()
db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        w_list = list()
        w_dict = {}
        for c in city.query.all():
            r = requests.get(f'http://api.openweathermap.org/data/2.5/find?q={c.name}&units=metric&appid=c017dede5fce581ea940ac5984eda868')
            json_dict = json.loads(r.text)
            w_dict = {
                'city': json_dict['list'][0]['name'],
                'id': c.id,
                'temp': round(json_dict['list'][0]['main']['temp']),
                'weather': json_dict['list'][0]['weather'][0]['main']
                }
            w_list.append(w_dict)
        return render_template('index.html', weather=w_list)
    elif request.method == 'POST':
        f_city = request.form['city_name']
        if f_city:
            w_city = city.query.filter_by(name=f_city).first()
            if w_city:
                flash("The city has already been added to the list!")
            else:
                r = requests.get(f'http://api.openweathermap.org/data/2.5/find?q={f_city}&units=metric&appid=c017dede5fce581ea940ac5984eda868')
                json_dict = json.loads(r.text)
                if json_dict['count'] == 0:
                    flash("The city doesn't exist!")
                else:
                    w_city = city(name=f'{f_city}')
                    db.session.add(w_city)
                    db.session.commit()
        return redirect('/')

@app.route('/delete/<city_id>', methods =['GET', 'POST'])
def delete(city_id):
    if request.method == 'POST':
        d_city = city.query.filter_by(id=city_id).first()
        db.session.delete(d_city)
        db.session.commit()
        return redirect('/')

# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
