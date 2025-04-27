# Mavericks Backend

This is a Flask-based backend application for the Mavericks project.


## Requirements
- Python 3.8 or higher
- Flask
- Virtualenv (optional but recommended)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/mavericks-backend.git
    cd mavericks-backend
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. Set the environment variables:
    ```bash
    export FLASK_APP=app.py
    export FLASK_ENV=development  # For development mode
    ```

    On Windows (Command Prompt):
    ```cmd
    set FLASK_APP=app.py
    set FLASK_ENV=development
    ```

2. Run the Flask development server:
    ```bash
    flask run
    ```

3. Open your browser and navigate to `http://127.0.0.1:5000`.


## License
This project is licensed under the MIT License. See the `LICENSE` file for details.