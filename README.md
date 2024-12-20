# Django Project Setup

## Overview  
This is a basic setup for a Django project with a Git repository, and an initial app structure. Follow the steps below to get started.

## Requirements 
- Python 3.x  
- pip  
- virtualenv (recommended for managing dependencies)  

## Setup Instructions  

### 1. Clone the repository  
Start by cloning the project repository:  
`git clone https://github.com/natinium/social-api.git`

### 2. Navigate into the project directory  
Change to the directory where the project was cloned:  
`cd social-api`

### 3. Create and activate a virtual environment  
Create a virtual environment to manage the project's dependencies:  
`python -m venv venv`

- **Activate on Windows:**  
  `venv\Scripts\activate`

- **Activate on macOS/Linux:**  
  `source venv/bin/activate`

### 4. Set up the database  
Run the migrations to set up your database:  
`python manage.py migrate`

### 5. Start the development server  
Once migrations are complete, start the development server:  
`python manage.py runserver`  

The development server should now be running at:  
http://127.0.0.1:8000/

## License  
This project is licensed under the MIT License.