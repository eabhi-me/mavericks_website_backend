from flask import render_template
from flask import request, jsonify
from application import app
from application.models import Member
from bson import ObjectId
from scripts.mdatabase import members_collection, projects_collection

def serialize_doc(doc):
    doc['_id'] = str(doc['_id'])
    return doc

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/members', methods=['GET', 'POST'])
def membersDetails():
    if request.method == 'GET':
        results = members_collection.find({})
        members = [serialize_doc(member) for member in results]
        return jsonify(members)
    elif request.method == 'POST':
        new_member = request.json
        projects_collection.insert_one(new_member)
        return jsonify({"message": "Member added successfully"}), 201

@app.route('/projects', methods=['GET', 'POST'])
def projectsDetails():
    if request.method == 'GET':
        results = projects_collection.find({})
        projects = [serialize_doc(project) for project in results]
        return jsonify(projects)
    elif request.method == 'POST':
        new_project = request.json
        projects_collection.insert_one(new_project)
        return jsonify({"message": "Project added successfully"}), 201
