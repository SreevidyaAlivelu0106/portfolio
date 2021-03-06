import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict
import re

load_dotenv()
app = Flask(__name__)
if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
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

@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline", url=os.getenv("URL"))


# @app.route('/api/timeline_post', methods=[ 'POST' ])
# def post_time_line_post():
#     name = request.form['name' ]
#     email = request.form['email']
#     content = request.form['content']
#     timeline_post = TimelinePost.create(name=name, email=email, content=content)
#     return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=[ 'POST' ])
def post_time_line_post():
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not request.form['name']:
        return "Invalid name", 400
    elif not (re.fullmatch(regex, request.form['email'])):
        return "Invalid email", 400
    elif not request.form['content']:
        return "Invalid content", 400
    else:        
        name = request.form['name']
        email = request.form['email']
        content = request.form['content']
        timeline_post = TimelinePost.create(name=name, email=email, content=content)
        return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=[ 'GET'])
def get_time_line_post():
    return {
    'timeline_posts': [
        model_to_dict(p)
        for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
     }

@app.route('/api/timeline_post', methods=[ 'DELETE'])
def delete_time_line_post():
    id = request.form['id']
    TimelinePost.delete_by_id(id)

    return "deleted successfully"
