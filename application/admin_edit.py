from application import app
from flask import jsonify, request
from flask_login import login_required
from .utils.data import iot_projects, events
import json
import os

# Helper function to save data to file
def save_data_to_file(data, filename):
    file_path = os.path.join(os.path.dirname(__file__), 'utils', filename)
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Convert data to Python list/dict string
    data_str = json.dumps(data, indent=4)
    # Replace the existing data with new data
    if filename == 'data.py':
        if 'iot_projects' in content:
            content = content.replace(
                content[content.find('iot_projects = ['):content.find(']', content.find('iot_projects = [')) + 1],
                f'iot_projects = {data_str}'
            )
        elif 'events' in content:
            content = content.replace(
                content[content.find('events = ['):content.find(']', content.find('events = [')) + 1],
                f'events = {data_str}'
            )
    
    with open(file_path, 'w') as f:
        f.write(content)

# IoT Projects Routes
@app.route('/api/iot-projects', methods=['GET'])
@login_required
def get_iot_projects():
    return jsonify(iot_projects)

@app.route('/api/iot-projects', methods=['POST'])
@login_required
def add_iot_project():
    data = request.json
    new_project = {
        'name': data['name'],
        'description': data['description']
    }
    iot_projects.append(new_project)
    save_data_to_file(iot_projects, 'data.py')
    return jsonify({'message': 'Project added successfully', 'project': new_project}), 201

@app.route('/api/iot-projects/<int:project_id>', methods=['DELETE'])
@login_required
def delete_iot_project(project_id):
    if project_id < 0 or project_id >= len(iot_projects):
        return jsonify({'error': 'Project not found'}), 404
    
    deleted_project = iot_projects.pop(project_id)
    save_data_to_file(iot_projects, 'data.py')
    return jsonify({'message': 'Project deleted successfully', 'project': deleted_project})

# Events Routes
@app.route('/api/events', methods=['GET'])
@login_required
def get_events():
    return jsonify(events)

@app.route('/api/events', methods=['POST'])
@login_required
def add_event():
    data = request.json
    new_event = {
        'id': len(events) + 1,
        'description': data['description'],
        'link': data['link']
    }
    events.append(new_event)
    save_data_to_file(events, 'data.py')
    return jsonify({'message': 'Event added successfully', 'event': new_event}), 201

@app.route('/api/events/<int:event_id>', methods=['DELETE'])
@login_required
def delete_event(event_id):
    event = next((e for e in events if e['id'] == event_id), None)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    events.remove(event)
    save_data_to_file(events, 'data.py')
    return jsonify({'message': 'Event deleted successfully', 'event': event})
