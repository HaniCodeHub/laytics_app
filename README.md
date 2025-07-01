# Class Manager Application

A comprehensive class management system built with Streamlit and PostgreSQL. This application provides user authentication, class management, student enrollment, and results tracking with interactive analytics.

## Features

- **User Authentication**: Secure login and signup system
- **Dashboard Analytics**: Interactive charts showing class distribution, performance overview, and enrollment trends
- **Class Management**: Create and manage classes with student enrollment
- **Results Management**: Add and track student results with performance analytics
- **Modern UI**: Responsive design with gradient styling and interactive Plotly charts

## Project Structure

```
class-manager/
│
├── main.py                 # Main application entry point
├── db_connection.py        # Database connection and table creation
├── login_system.py         # Authentication system
├── home_page.py           # Landing page with features showcase
├── dashboard.py           # Analytics dashboard
├── class_manager.py       # Class and results management
│
├── .streamlit/
│   └── config.toml        # Streamlit configuration
│
├── assets/
│   └── img3.png          # Application logo/image
│
├── local_requirements.txt # Python dependencies
└── README.md             # This file
```

## Prerequisites

Before running this application, ensure you have:

1. **Python 3.8 or higher** installed
2. **PostgreSQL** database server installed and running
3. **Git** (optional, for cloning)

## Installation & Setup

### Step 1: Clone or Download the Project

```bash
# Option 1: Clone from repository (if available)
git clone <repository-url>
cd class-manager

# Option 2: Create directory and add files manually
mkdir class-manager
cd class-manager
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r local_requirements.txt
```

### Step 4: Database Setup

#### Install PostgreSQL
- **Windows**: Download from https://www.postgresql.org/download/windows/
- **macOS**: Use Homebrew: `brew install postgresql`
- **Linux**: Use package manager: `sudo apt-get install postgresql postgresql-contrib`

#### Create Database

```sql
-- Connect to PostgreSQL as superuser
psql -U postgres

-- Create database
CREATE DATABASE class_manager;

-- Create user (optional, or use existing user)
CREATE USER class_manager_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE class_manager TO class_manager_user;

-- Exit psql
\q
```

### Step 5: Configure Environment Variables

Create a `.env` file in the project root or set environment variables:

```bash
# Option 1: Create .env file (you'll need to install python-dotenv)
echo "PGHOST=localhost" > .env
echo "PGDATABASE=class_manager" >> .env
echo "PGUSER=postgres" >> .env
echo "PGPASSWORD=your_postgresql_password" >> .env
echo "PGPORT=5432" >> .env

# Option 2: Set environment variables directly
# Windows Command Prompt:
set PGHOST=localhost
set PGDATABASE=class_manager
set PGUSER=postgres
set PGPASSWORD=your_postgresql_password
set PGPORT=5432

# Windows PowerShell:
$env:PGHOST="localhost"
$env:PGDATABASE="class_manager"
$env:PGUSER="postgres"
$env:PGPASSWORD="your_postgresql_password"
$env:PGPORT="5432"

# macOS/Linux:
export PGHOST=localhost
export PGDATABASE=class_manager
export PGUSER=postgres
export PGPASSWORD=your_postgresql_password
export PGPORT=5432
```

### Step 6: Create Streamlit Configuration

Create the `.streamlit` directory and configuration file:

```bash
mkdir .streamlit
```

Create `.streamlit/config.toml`:

```toml
[server]
headless = true
address = "0.0.0.0"
port = 8501

[theme]
base = "dark"
```

## Running the Application

### Method 1: Direct Run

```bash
streamlit run main.py
```

### Method 2: Specify Port

```bash
streamlit run main.py --server.port 8501
```

The application will be available at: `http://localhost:8501`

## Usage Guide

### 1. First Time Setup
- Open the application in your browser
- The database tables will be created automatically on first run

### 2. User Registration
- Click "Sign Up" on the homepage
- Fill in email, username, and password
- Click "Sign Up" to create account

### 3. Login
- Click "Login" on the homepage
- Enter your credentials
- Access the main application

### 4. Using the Application

#### Dashboard
- View analytics with three tabs:
  - **Class Distribution**: Bar chart of students per class
  - **Performance Overview**: Line chart of class averages
  - **Enrollment Trends**: Pie chart of enrollment distribution

#### Add New Class
- Enter class name and semester
- Add students with roll numbers and names
- Click "Save Class"

#### Results Management
- Select a class from the grid
- Enter subject name and total marks
- Input marks for each student
- Generate results with performance analytics

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify PostgreSQL is running
   - Check environment variables
   - Ensure database exists

2. **Port Already in Use**
   - Change port in command: `streamlit run main.py --server.port 8502`
   - Or modify `.streamlit/config.toml`

3. **Module Import Errors**
   - Ensure virtual environment is activated
   - Reinstall dependencies: `pip install -r local_requirements.txt`

4. **Permission Errors (Windows)**
   - Run Command Prompt as Administrator
   - Or use PowerShell with appropriate permissions

### Database Reset

If you need to reset the database:

```sql
-- Connect to PostgreSQL
psql -U postgres -d class_manager

-- Drop and recreate tables
DROP TABLE IF EXISTS results CASCADE;
DROP TABLE IF EXISTS students CASCADE;
DROP TABLE IF EXISTS classes CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Exit and restart the application to recreate tables
\q
```

## Development

### Project Architecture

- **main.py**: Application entry point and session management
- **db_connection.py**: Database abstraction layer
- **login_system.py**: Authentication and user management
- **home_page.py**: Landing page with feature showcase
- **dashboard.py**: Analytics dashboard with interactive charts
- **class_manager.py**: Core functionality for class and results management

### Adding Features

1. Create new Python modules following the existing pattern
2. Import and integrate in `main.py`
3. Update navigation in `class_manager.py` if needed
4. Follow the existing PostgreSQL patterns for database operations

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all prerequisites are installed
3. Ensure database connection is properly configured
4. Check that all environment variables are set correctly

## License

This project is for educational purposes. Modify and distribute as needed.