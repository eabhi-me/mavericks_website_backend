from application import app
from flask import redirect, url_for, render_template, flash, jsonify, session, request
from .form import LoginForm, RegisterForm
from config.mdatabase import users_collection, projects_collection, latest_news_collection
from .extensions import bcrypt
from flask_login import login_user, logout_user, current_user, login_required
from application import User
from bson import ObjectId
from datetime import datetime
from .utils.data import iot_projects, events


@app.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_authenticated:
        flash('Please log in to access the dashboard.', category='warning')
        return redirect(url_for('login'))
    
    # Get all projects
    # projects = list(projects_collection.find())
    projects = iot_projects
    
    # Get all users
    users = list(users_collection.find())
    
    # Get all news
    # news = list(latest_news_collection.find())
    news = events
    
    return render_template('dashboard.html', projects=projects, users=users, news=news)


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = users_collection.find_one({'email_address': form.email_address.data})
        if user:
            if bcrypt.check_password_hash(user['password'], form.password.data):
                user_obj = User(user)
                login_user(user_obj, remember=True)  # Enable remember me
                session.permanent = True  # Make session permanent
                flash('Login successful!', category='success')
                return redirect(url_for('dashboard'))
            else:
                flash('Incorrect password. Please try again.', category='danger')
        else:
            flash('User not found. Please check your email address.', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    # Clear the user session
    session.clear()
    # Logout the user
    logout_user()
    # Clear any flash messages
    flash('You have been successfully logged out.', 'success')
    # Redirect to login page
    return redirect(url_for('login'))

@app.route('/user/<string:user_name>', methods=['GET'])
def viewUser(user_name):
    user = users_collection.find_one({'username': user_name})
    if user:
        user['_id'] = str(user['_id'])  # Convert ObjectId to string for JSON serialization
        return jsonify(user), 200
    else:
        return jsonify({'error': 'User not found'}), 404
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    print("Form submitted:", form.is_submitted())
    print("Form validated:", form.validate_on_submit())
    if form.validate_on_submit():
        print("Form data:", {
            'username': form.username.data,
            'email': form.email_address.data,
            'password_length': len(form.password.data) if form.password.data else 0
        })
        existing_user = users_collection.find_one({'email_address': form.email_address.data})
        if existing_user:
            print("User already exists with email:", form.email_address.data)
            flash('Email address already exists. Please use a different one.', category='error')
            return render_template('register.html', form=form)
        
        try:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            print("Generated password hash:", hashed_password)
            new_user = {
                'username': form.username.data,
                'email_address': form.email_address.data,
                'password': hashed_password,
                'role': 'User'  # Default role for new users
            }
            print("Attempting to insert new user:", new_user)
            result = users_collection.insert_one(new_user)
            print("Insert result:", result.inserted_id)
            flash('Registration successful! You can now log in.', category='success')
            return redirect(url_for('login'))
        except Exception as e:
            print("Error during registration:", str(e))
            flash('An error occurred during registration. Please try again.', category='error')
            return render_template('register.html', form=form)
    else:
        if form.errors:
            print("Form validation errors:", form.errors)
    
    return render_template('register.html', form=form)

