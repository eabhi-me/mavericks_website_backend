from flask import render_template, flash, redirect, url_for
from flask import request, jsonify
from application import app
from bson import ObjectId
from config.mdatabase import members_collection, projects_collection
from .utils.data import coordintors, iot_projects, members, events, members_old, diploma_members
from .form import LoginForm
from flask_login import login_user, logout_user, current_user, login_required

# For converting the id of mangodb to serializable
def serialize_doc(doc):
    doc['_id'] = str(doc['_id'])
    return doc

@app.route('/')
@app.route('/home')
def home():
    items = members
    return render_template('index.html', coordintors=coordintors, items=items, events=events)
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/projects')
def project():
    return render_template('projects.html', iot_projects=iot_projects)

@app.route('/teams')
def team():
    return render_template('team.html', members=members, members_old=members_old, diploma_members=diploma_members)



@app.route('/gallery')
def gallery():
    total_images = 10
    return render_template('gallery.html',total_images=total_images)

