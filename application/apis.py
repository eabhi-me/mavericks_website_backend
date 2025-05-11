from flask import render_template, flash, redirect, url_for
from flask import request, jsonify
from application import app, mail
from bson import ObjectId
from config.mdatabase import members_collection, projects_collection
from .utils.data import coordintors, iot_projects, members, events, members_old, diploma_members, gallery
from .utils.member_data import batch25_members, batch26_members, batch27_members, ICD_members
from .form import LoginForm
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Mail, Message

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
    return render_template('team.html', batch25_members=batch25_members, batch26_members=batch26_members, batch27_members=batch27_members, diploma_members=ICD_members)

@app.route('/gallery')
def gallery_route():
    return render_template('gallery.html', gallery=gallery)

@app.route('/contact-send', methods=['GET', 'POST'])
def contact_send():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            subject = request.form.get('subject')
            message = request.form.get('message')

            # Create email message
            msg = Message(
                subject=f"Contact Form: {subject}",
                recipients=[app.config['MAIL_USERNAME']],  # Send to your email
                body=f"""
                New contact form submission:
                
                Name: {name}
                Email: {email}
                Subject: {subject}
                
                Message:
                {message}
                """
            )
            
            # Send email
            mail.send(msg)
            
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('contact'))
            
        except Exception as e:
            flash('An error occurred while sending your message. Please try again later.', 'danger')
            return redirect(url_for('contact'))
            
    return render_template('contact.html')