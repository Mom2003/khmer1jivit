# Nassa Task Management API

A simple, lightweight Task/Todo Management system built using FastAPI and Python 3.14. It features a complete RESTful interface with CRUD operations and in-memory persistence.

## Features

- **Create Task**: Add new tasks with title and optional description.
- **List Tasks**: Fetch all tasks, with optional filtering by status (`todo`, `in_progress`, `done`).
- **Get Task**: View a specific task by its UUID.
- **Update Task**: Modify a task's title, description, or status.
- **Delete Task**: Remove a task.
- **API Documentation**: Automated interactive API docs powered by Swagger UI and ReDoc.

## Getting Started

### Prerequisites

- Python >= 3.14
- [Poetry](https://python-poetry.org/)

### Installation

1. Install the project dependencies:
   ```bash
   poetry install
   ```

### Running the Application

1. Start the development server using Uvicorn:
   ```bash
   poetry run uvicorn nassa.main:app --reload
   ```

2. Open your browser and navigate to:
   - **Interactive Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - **ReDoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
   - **Root API Endpoint**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### Running Tests

To run the unit tests, execute:
   ```bash
   poetry run pytest
   ```
