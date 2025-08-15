# IESCP V2 - Influencer Engagement & Sponsorship Coordination Platform

The Influencer Engagement & Sponsorship Coordination Platform (IESCP) V2 is a multi-user web application designed to connect influencers and sponsors. It enables influencers to explore ad campaigns and sponsors to create and manage campaigns and ad requests, facilitating seamless collaboration.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [API Design](#api-design)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Running the Application](#running-the-application)

## Overview
IESCP V2 is a robust platform that streamlines interactions between influencers, sponsors, and administrators. Influencers can discover and negotiate ad campaigns, sponsors can manage campaigns and communicate with influencers, and administrators can oversee platform activities and ensure smooth operations.

## Features
- **User Authentication**: Secure signup and login for influencers, sponsors, and administrators.
- **Admin Dashboard**: Admins can approve sponsor accounts, monitor platform statistics, and block suspicious activities.
- **Influencer Tools**: Influencers can browse, search, and negotiate campaigns and ad requests, as well as chat with sponsors.
- **Sponsor Capabilities**: Sponsors can create, read, update, and delete campaigns and ad requests, and communicate with influencers.
- **Performance Optimization**: Caching with Redis to enhance API performance.
- **Asynchronous Processing**: Celery for handling heavy backend tasks and Celery Beat for scheduling automated emails and reminders.

## Technologies Used
- **Python**: Core programming language for backend development.
- **Flask**: Framework for building the backend and RESTful APIs.
- **SQLite**: Lightweight database for storing application data.
- **Vue.js 3**: Frontend framework for creating dynamic user interfaces.
- **Jinja2**: Templating engine for rendering dynamic HTML content.
- **Bootstrap**: CSS framework for responsive and visually appealing designs.
- **Redis**: In-memory data store for caching and Celery backend.
- **Celery & Celery Beat**: Tools for asynchronous task processing and task scheduling.
- **MailHog**: Local SMTP server for testing email functionality.
- **Flask-RESTful**: Extension for building REST APIs.
- **Flask-SQLAlchemy**: ORM for database interactions.
- **Flask-JWT-Extended**: Authentication and authorization for API endpoints.

## Architecture
IESCP V2 follows the **Model-View-Controller (MVC)** architecture:
- **Model**: Python classes mapped to SQLite database tables using Flask-SQLAlchemy.
- **View**: Frontend built with Vue.js 3, enhanced with Bootstrap for responsive design.
- **Controller**: Flask-based backend handling API requests and business logic.

The application leverages Redis for caching to improve performance and Celery for asynchronous task execution, ensuring scalability and responsiveness.

## Project Structure
```
IESCP/
├── backend/                # Flask backend code
│   ├── app.py             # Main Flask application
│   ├── requirements.txt   # Backend dependencies
│   └── ...                # Other backend files (models, routes, etc.)
├── frontend/               # Vue.js frontend code
│   ├── package.json       # Frontend dependencies
│   ├── src/               # Vue.js source files
│   └── ...                # Other frontend files
├── README.md              # Project documentation
└── ...                    # Additional configuration files
```

## API Design
The APIs are built using **Flask-RESTful** to perform CRUD (Create, Read, Update, Delete) operations on resources such as:
- Users
- Influencer Profiles
- Sponsor Profiles
- Campaigns
- Ad Requests

Authentication and authorization are implemented using **Flask-JWT-Extended**, ensuring secure access to API endpoints. APIs are designed to be RESTful, with clear endpoints and standardized response formats.

## Prerequisites
Before setting up the project, ensure you have the following installed:
- **Python 3.8+**: For backend development.
- **Node.js 14+ and npm**: For frontend development.
- **Redis**: For caching and Celery backend.
- **MailHog**: For local email testing.
- **Git**: For cloning the repository.

## Installation and Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ikrlalit/IESCP.git
   cd IESCP
   cd IESCP
   ```

2. **Backend Setup**:
   - Navigate to the `backend` directory:
     ```bash
     cd backend
     ```
   - Create and activate a virtual environment:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate  # On Windows: .venv\Scripts\activate
     ```
   - Install backend dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. **Frontend Setup**:
   - Navigate to the `frontend` directory:
     ```bash
     cd ../frontend
     ```
   - Install frontend dependencies:
     ```bash
     npm install
     ```

4. **Install Redis**:
   - Follow the official Redis installation guide for your operating system: [Redis Installation](https://redis.io/docs/install/install-redis/).
   - Ensure the Redis server is running:
     ```bash
     redis-server
     ```

5. **Install MailHog**:
   - Download and install MailHog: [MailHog Installation](https://github.com/mailhog/MailHog).
   - Start MailHog:
     ```bash
     ~/go/bin/MailHog
     ```

## Running the Application
1. **Start the Flask Backend**:
   - In the `backend` directory, with the virtual environment activated:
     ```bash
     python app.py
     ```
   - The Flask server will run on `http://localhost:5000` (or as configured).

2. **Start the Vue.js Frontend**:
   - In the `frontend` directory:
     ```bash
     npm run serve
     ```
   - The frontend will be available at `http://localhost:8080` (or as configured).

3. **Start Celery Worker**:
   - In a new terminal, navigate to the `backend` directory and activate the virtual environment:
     ```bash
     celery -A app:celery_app worker --loglevel INFO
     ```

4. **Start Celery Beat**:
   - In another terminal, navigate to the `backend` directory:
     ```bash
     celery -A app:celery_app beat --loglevel INFO
     ```

5. **Access the Application**:
   - Open `http://localhost:8080` in your browser to interact with the application.
   - Use MailHog’s web interface (`http://localhost:8025`) to view emails sent during testing.

