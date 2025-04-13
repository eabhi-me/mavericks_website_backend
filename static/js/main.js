document.addEventListener('DOMContentLoaded', function() {
    fetch('http://127.0.0.1:5000/projects')
        .then(response => response.json())
        .then(data => {
            console.log(data.message)
            const newSection = document.getElementById('news-section');
            const paragraph = document.createElement('p');
            paragraph.textContent = data[0].message; // Assuming the response has a 'message' field
            newSection.appendChild(paragraph);
        })
        .catch(error => console.error('Error fetching data:', error));
});

async function fetchProjects() {
    try {
      const response = await fetch('http://127.0.0.1:5000/projects');
      const projects = await response.json();

      const projectGrid = document.getElementById('project-grid');
      if (!projectGrid) {
        console.error('Error: Element with ID "project-grid" not found.');
        return;
      }
      projects.forEach(project => {
        console.log(project)
        const projectCard = document.createElement('div');
        projectCard.className = 'col-md-4 mb-4';

        projectCard.innerHTML = `
          <div class="card h-100">
            <img src="${project.image}" class="card-img-top" alt="${project.title}">
            <div class="card-body">
              <h5 class="card-title">${project.title}</h5>
              <p class="card-text">${project.description}</p>
            </div>
          </div>
        `;

        projectGrid.appendChild(projectCard);
      });
    } catch (error) {
      console.error('Error fetching projects:', error);
    }
  }
