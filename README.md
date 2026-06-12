# Chatbot

A full-stack chatbot application built with FastAPI and React/Vue (Frontend).

## Project Structure

- `backend/`: FastAPI application containing the core API logic.
- `frontend/`: User interface for the chatbot.
- `docker-compose.yml`: Docker configuration to easily run the entire stack.
- `env/`: Python virtual environment (if running locally).

## How to Run

### Using Docker (Recommended)

1. Make sure you have Docker and Docker Compose installed.
2. Run the following command in the root directory:
   ```bash
   docker-compose up --build
   ```

### Running Locally (Backend)

1. Activate the virtual environment:
   ```bash
   source env/bin/activate
   ```
2. Navigate to the backend directory and run the server:
   ```bash
   cd backend
   python main.py
   ```

## Requirements

- Python 3.x
- Docker (optional but recommended)
