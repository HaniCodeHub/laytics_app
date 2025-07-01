# Class Manager Application

## Overview

This is a Class Manager application built with Streamlit that provides a web-based interface for managing classes and students. The application features user authentication, a dashboard for analytics, and functionality to create classes and manage student data. The system is designed with a modular architecture separating concerns between authentication, data management, and user interface components.

## System Architecture

The application follows a layered architecture pattern with clear separation between:

1. **Presentation Layer**: Streamlit-based web interface with multiple page components
2. **Business Logic Layer**: Core application logic for class and student management
3. **Data Access Layer**: Database connection and query management using PostgreSQL
4. **Authentication Layer**: User login/signup system with password hashing

The architecture emphasizes modularity with distinct classes handling specific responsibilities, making the codebase maintainable and extensible.

## Key Components

### Frontend Architecture
- **Streamlit Framework**: Web application framework providing reactive UI components
- **Multi-page Navigation**: Sidebar-based navigation between Home Dashboard, Add New Class, and Results Management
- **Custom CSS Styling**: Enhanced UI with custom styles for professional appearance
- **Responsive Design**: Layout adapts to different screen sizes using Streamlit's column system

### Backend Architecture
- **Class-based Design**: Object-oriented approach with separate classes for different functionalities
- **Database Abstraction**: `Connect_DB` class provides centralized database connection management
- **Session Management**: Streamlit session state for maintaining user authentication and application state

### Core Classes
1. **ClassManager**: Main application controller handling navigation and core functionality
2. **Dashboard**: Analytics and metrics display with database-driven insights
3. **Login**: Authentication system with user registration and login capabilities
4. **ClassManagerApp**: Home page and initial application entry point

## Data Flow

1. **Application Initialization**: 
   - Database tables are created if they don't exist
   - Session state variables are initialized
   - User authentication status is checked

2. **Authentication Flow**:
   - Users can sign up with email, username, and password
   - Passwords are hashed using SHA-256 before storage
   - Login credentials are verified against the database
   - Successful authentication sets session state for access control

3. **Main Application Flow**:
   - Authenticated users access the main ClassManager interface
   - Navigation between different modules via sidebar selection
   - Database operations are performed through the Connect_DB class
   - Real-time data fetching for dashboard metrics and class management

## External Dependencies

### Core Framework
- **Streamlit**: Web application framework and UI components
- **psycopg2**: PostgreSQL database adapter with RealDictCursor for enhanced query results

### Data Visualization
- **pandas**: Data manipulation and analysis
- **matplotlib**: Static plotting library for charts and graphs
- **seaborn**: Statistical data visualization built on matplotlib
- **plotly**: Interactive plotting library for enhanced user experience

### Security and Utilities
- **hashlib**: Password hashing for secure authentication
- **os**: Environment variable management for configuration

### Database Schema
The application uses PostgreSQL with the following main tables:
- **users**: User authentication data (id, email, username, password, created_at)
- **classes**: Class information storage
- **students**: Student records linked to classes

## Deployment Strategy

The application is designed for cloud deployment with environment variable configuration:

### Database Configuration
- Uses environment variables for PostgreSQL connection parameters
- Default fallback values for local development
- Connection pooling through psycopg2 with proper error handling

### Environment Variables
- `PGHOST`: Database host (default: localhost)
- `PGDATABASE`: Database name (default: class_manager)
- `PGUSER`: Database user (default: postgres)
- `PGPASSWORD`: Database password
- `PGPORT`: Database port (default: 5432)

### Deployment Considerations
- Application state managed through Streamlit session state
- Database connection management with proper error handling
- Modular design allows for easy scaling and maintenance

## Changelog

```
Changelog:
- July 01, 2025. Initial setup
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```