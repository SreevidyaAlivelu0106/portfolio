import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)
mydb=MySQLDatabase(os.getenv("MYSQL_DATABASE"),
    user=os.getenv ( "MYSQL_USER"),
    password=os.getenv ( "MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306
)

class TimelinePost (Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

print (mydb)
@app.route('/')
def index():
    return render_template('workex_ed_sree.html', title="Sree Info", url=os.getenv("URL"))


@app.route('/sree_hobbies')
def sree_hobbies():
    return render_template('hobbies_template_sree.html', title="sree's Hobbies", url=os.getenv("URL"))


@app.route('/api/timeline_post', methods=[ 'POST' ])
def post_time_line_post():
    name = request.form['name' ]
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=[ 'GET'])
def get_time_line_post():
    return {
    'timeline _posts': [
        model_to_dict(p)
        for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
     }


@app.route('/api/timeline_post/<id>', methods=['DELETE'])
def delete_time_line_post(id):
    #p = TimelinePost.get(TimelinePost.id == id)

    TimelinePost.delete(TimelinePost.id == id)
    TimelinePost.commit()
    return "deleted"
