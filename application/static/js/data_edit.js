// Project Management Functions
async function editProject(id) {
    const project = await fetch(`/api/projects/${id}`).then(res => res.json());
    const modal = new bootstrap.Modal(document.getElementById('addProjectModal'));
    const form = document.getElementById('addProjectForm');
    
    form.name.value = project.name;
    form.description.value = project.description;
    
    form.onsubmit = async (e) => {
        e.preventDefault();
        const data = {
            name: form.name.value,
            description: form.description.value
        };
        
        await fetch(`/api/projects/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        location.reload();
    };
    
    modal.show();
}

async function deleteProject(id) {
    if (confirm('Are you sure you want to delete this project?')) {
        await fetch(`/api/projects/${id}`, { method: 'DELETE' });
        location.reload();
    }
}

async function submitProject() {
    const form = document.getElementById('addProjectForm');
    const data = {
        name: form.name.value,
        description: form.description.value
    };
    
    await fetch('/api/projects', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    
    location.reload();
}

// User Management Functions
async function editUser(id) {
    const user = await fetch(`/api/users/${id}`).then(res => res.json());
    const modal = new bootstrap.Modal(document.getElementById('addUserModal'));
    const form = document.getElementById('addUserForm');
    
    form.username.value = user.username;
    form.email.value = user.email_address;
    form.role.value = user.role;
    
    form.onsubmit = async (e) => {
        e.preventDefault();
        const data = {
            username: form.username.value,
            email: form.email.value,
            role: form.role.value
        };
        
        if (form.password.value) {
            data.password = form.password.value;
        }
        
        await fetch(`/api/users/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        location.reload();
    };
    
    modal.show();
}

async function deleteUser(id) {
    if (confirm('Are you sure you want to delete this user?')) {
        await fetch(`/api/users/${id}`, { method: 'DELETE' });
        location.reload();
    }
}

async function submitUser() {
    const form = document.getElementById('addUserForm');
    const data = {
        username: form.username.value,
        email: form.email.value,
        password: form.password.value,
        role: form.role.value
    };
    
    await fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    
    location.reload();
}

// News Management Functions
async function editNews(id) {
    const news = await fetch(`/api/news/${id}`).then(res => res.json());
    const modal = new bootstrap.Modal(document.getElementById('addNewsModal'));
    const form = document.getElementById('addNewsForm');
    
    form.title.value = news.title;
    form.description.value = news.description;
    form.date.value = news.date;
    
    form.onsubmit = async (e) => {
        e.preventDefault();
        const data = {
            title: form.title.value,
            description: form.description.value,
            date: form.date.value
        };
        
        await fetch(`/api/news/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        location.reload();
    };
    
    modal.show();
}

async function deleteNews(id) {
    if (confirm('Are you sure you want to delete this news item?')) {
        await fetch(`/api/news/${id}`, { method: 'DELETE' });
        location.reload();
    }
}

async function submitNews() {
    const form = document.getElementById('addNewsForm');
    const data = {
        title: form.title.value,
        description: form.description.value,
        date: form.date.value
    };
    
    await fetch('/api/news', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    
    location.reload();
}

// IoT Projects Management
async function deleteIoTProject(index) {
    if (confirm('Are you sure you want to delete this project?')) {
        try {
            const response = await fetch(`/api/iot-projects/${index}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                location.reload();
            } else {
                alert('Failed to delete project');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while deleting the project');
        }
    }
}

async function submitIoTProject() {
    const form = document.getElementById('addProjectForm');
    const data = {
        name: form.name.value,
        description: form.description.value
    };
    
    try {
        const response = await fetch('/api/iot-projects', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            location.reload();
        } else {
            alert('Failed to add project');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while adding the project');
    }
}

// Events Management
async function deleteEvent(id) {
    if (confirm('Are you sure you want to delete this event?')) {
        try {
            const response = await fetch(`/api/events/${id}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                location.reload();
            } else {
                alert('Failed to delete event');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while deleting the event');
        }
    }
}

async function submitEvent() {
    const form = document.getElementById('addNewsForm');
    const data = {
        description: form.description.value,
        link: form.title.value
    };
    
    try {
        const response = await fetch('/api/events', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            location.reload();
        } else {
            alert('Failed to add event');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while adding the event');
    }
}
