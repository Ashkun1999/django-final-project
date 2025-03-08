# Task Management Application

## Project Overview

This is a web-based task management application built with Django. The application allows users to create, assign, and track tasks in a collaborative environment. It provides a simple and intuitive interface for managing tasks, setting priorities, and tracking progress toward completion.

## Features

- **User Management**
  - User registration and authentication
  - User profile management
  - Secure password handling

- **Task Management**
  - Create, edit, and delete tasks
  - Add detailed descriptions to tasks
  - Set due dates and deadlines
  - Categorize tasks with labels or tags

- **Task Assignment**
  - Assign tasks to specific users
  - Reassign tasks as needed
  - Track task ownership and responsibility

- **Priority System**
  - Set task priorities (High, Medium, Low)
  - Visual indicators for different priority levels
  - Sort and filter tasks by priority

- **Progress Tracking**
  - Mark tasks as in-progress or completed
  - Track completion dates
  - View task history and changes
  - Generate reports on task completion statistics

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Installation Steps

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/task-management.git
   cd task-management
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```
   python manage.py migrate
   ```

5. Create a superuser (admin):
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at `http://localhost:8000`

## Usage

### User Registration and Login
- Navigate to the application URL
- Click on "Register" to create a new account
- Log in with your credentials

### Task Management
- Create a new task by clicking "New Task" button
- Fill in task details including title, description, due date, and priority
- Assign the task to yourself or another user
- View all tasks on the dashboard
- Click on a task to view details or edit

### Task Filtering and Sorting
- Use filters to view tasks by priority, status, or assignee
- Sort tasks by due date, creation date, or priority
- Search for specific tasks using the search bar

### Task Completion
- Mark tasks as "In Progress" when you start working on them
- Mark tasks as "Completed" when finished
- View completion statistics in the reports section

## Technologies Used

- **Backend**
  - Django 4.x: Python web framework
  - Django REST Framework: For API endpoints
  - SQLite/PostgreSQL: Database

- **Frontend**
  - HTML5, CSS3, JavaScript
  - Bootstrap: Responsive UI components
  - jQuery: DOM manipulation

- **Authentication**
  - Django Authentication System
  - JWT (JSON Web Tokens) for secure API authentication


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

