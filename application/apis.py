from flask import render_template, flash, redirect, url_for
from flask import request, jsonify
from application import app
from application.models import Member
from bson import ObjectId
from scripts.mdatabase import members_collection, projects_collection
from .utils.data import coordintors, iot_projects, members, events, members_old, diploma_members
from .models import User
from .form import LoginForm
from flask_login import login_user, logout_user, current_user, login_required

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

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email_address = form.email_address.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password = form.password.data):
            if not attempted_user.is_verified:
                flash('Please verify your email before logging in.', category='warning')
                return redirect(url_for('verify_user', email_address=attempted_user.email_address))
            login_user(attempted_user)
            flash(f'Success! You have loged in as {attempted_user.email_address}', category='info')
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect Email address or password', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been Logout',category='info')
    return redirect(url_for('login'))

@app.route('/gallery')
def gallery():
    total_images = 10
    return render_template('gallery.html',total_images=total_images)

# @app.route('/project')
# def project():
#     if request.method == 'GET':
#         results = projects_collection.find({})
#         projects = [serialize_doc(project) for project in results]
#     return render_template('projects.html', projects=projects)

# @app.route('/team')
# def team():
#     if request.method == 'GET':
#         results = members_collection.find({})
#         members = [serialize_doc(member) for member in results]
#         for member in members:
#             if "image_url" in member:
#                 try:
#                     file_id = member["image_url"].split("/d/")[1].split("/")[0]
#                     member["image_direct"] = f"https://drive.google.com/uc?export=view&id={file_id}"
#                     print(member["image_direct"])
#                     print(file_id)
#                 except:
#                     member["image_direct"] = ""
#     return render_template('team.html', members=members)


# @app.route('/members', methods=['GET', 'POST'])
# def membersDetails():
#     if request.method == 'GET':
#         results = members_collection.find({})
#         members = [serialize_doc(member) for member in results]
#         return jsonify(members)
#     elif request.method == 'POST':
#         new_member = request.json
#         projects_collection.insert_one(new_member)
#         return jsonify({"message": "Member added successfully"}), 201

# @app.route('/projects', methods=['GET', 'POST'])
# def projectsDetails():
#     if request.method == 'GET':
#         results = projects_collection.find({})
#         projects = [serialize_doc(project) for project in results]
#         return jsonify(projects)
#     elif request.method == 'POST':
#         new_project = request.json
#         projects_collection.insert_one(new_project)
#         return jsonify({"message": "Project added successfully"}), 201
