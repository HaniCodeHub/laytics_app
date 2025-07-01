# Local Deployment Guide for Class Manager Application

## 🚀 Quick Start (3 Steps)

### For Windows Users:
1. **Download all project files** to a folder called `class-manager`
2. **Install PostgreSQL** from https://www.postgresql.org/download/windows/
3. **Double-click `run_windows.bat`** to set up and start the application

### For Mac/Linux Users:
1. **Download all project files** to a folder called `class-manager`
2. **Install PostgreSQL** (Homebrew: `brew install postgresql`, Ubuntu: `sudo apt install postgresql`)
3. **Run `./run_unix.sh`** in terminal to set up and start the application

---

## 📁 Complete File Structure

Here's what your `class-manager` folder should contain:

```
class-manager/
│
├── main.py                    # Main application entry point
├── db_connection.py          # PostgreSQL database connection
├── login_system.py           # User authentication system  
├── home_page.py             # Landing page with analytics preview
├── dashboard.py             # Main analytics dashboard
├── class_manager.py         # Class and results management
│
├── .streamlit/
│   └── config.toml          # Streamlit configuration
│
├── local_requirements.txt   # Python package dependencies
├── README.md               # Detailed documentation
├── DEPLOYMENT_GUIDE.md     # This file
├── setup_local.py          # Automated setup script
├── run_windows.bat         # Windows launcher
├── run_unix.sh            # Mac/Linux launcher
│
└── .env.template          # Environment variables template
```

---

## 📋 Prerequisites Checklist

### ✅ Software Requirements:
- [ ] **Python 3.8+** (Check: `python --version`)
- [ ] **PostgreSQL** (Any recent version)
- [ ] **Git** (Optional, for downloading)

### ✅ System Requirements:
- [ ] **4GB RAM** minimum
- [ ] **1GB free disk space**
- [ ] **Internet connection** (for package installation)

---

## 🔧 Detailed Setup Instructions

### Step 1: Install Prerequisites

#### Install Python:
- **Windows**: Download from https://python.org/downloads/
- **macOS**: Use Homebrew: `brew install python3`
- **Linux**: Usually pre-installed, or: `sudo apt install python3`

#### Install PostgreSQL:
- **Windows**: Download installer from PostgreSQL website
- **macOS**: `brew install postgresql && brew services start postgresql`
- **Linux**: `sudo apt install postgresql postgresql-contrib`

### Step 2: Download Project Files

Create a new folder and add all the project files listed in the structure above.

### Step 3: Environment Configuration

#### Option A: Use Environment Variables
Set these variables in your system:

**Windows (Command Prompt):**
```cmd
set PGHOST=localhost
set PGDATABASE=class_manager
set PGUSER=postgres
set PGPASSWORD=your_postgres_password
set PGPORT=5432
```

**Windows (PowerShell):**
```powershell
$env:PGHOST="localhost"
$env:PGDATABASE="class_manager"
$env:PGUSER="postgres"
$env:PGPASSWORD="your_postgres_password"
$env:PGPORT="5432"
```

**Mac/Linux:**
```bash
export PGHOST=localhost
export PGDATABASE=class_manager
export PGUSER=postgres
export PGPASSWORD=your_postgres_password
export PGPORT=5432
```

#### Option B: Use .env File
1. Copy `.env.template` to `.env`
2. Edit `.env` with your PostgreSQL credentials

### Step 4: Run the Application

#### Automated Setup (Recommended):
```bash
# Run the setup script
python setup_local.py

# Then start the application
streamlit run main.py
```

#### Manual Setup:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r local_requirements.txt

# Start application
streamlit run main.py
```

#### Using Launcher Scripts:
- **Windows**: Double-click `run_windows.bat`
- **Mac/Linux**: Run `./run_unix.sh` in terminal

---

## 🌐 Accessing the Application

Once started, the application will be available at:
- **Local URL**: http://localhost:8501
- **Network URL**: http://YOUR_IP:8501 (for network access)

---

## 🔍 Troubleshooting

### Database Connection Issues:

**Problem**: "Database connection failed"
**Solution**:
1. Verify PostgreSQL is running
2. Check your password in environment variables
3. Ensure database user has proper permissions

**Command to test connection**:
```bash
psql -h localhost -U postgres -d class_manager
```

### Port Already in Use:

**Problem**: "Port 8501 is already in use"
**Solution**:
```bash
streamlit run main.py --server.port 8502
```

### Package Installation Issues:

**Problem**: "Failed to install packages"
**Solution**:
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Then install packages
pip install -r local_requirements.txt
```

### Permission Issues (Windows):

**Problem**: "Access denied" or permission errors
**Solution**:
- Run Command Prompt as Administrator
- Or use PowerShell with elevated permissions

---

## 🎯 Usage Workflow

### First Time Setup:
1. **Access Application**: Open http://localhost:8501
2. **Sign Up**: Create a new user account
3. **Login**: Use your credentials to access the system

### Using the Application:

#### 1. Dashboard (Home):
- View overall statistics
- Analyze class distribution
- Check performance trends
- Monitor enrollment data

#### 2. Add New Class:
- Navigate to "Add New Class"
- Enter class name and semester
- Add students with roll numbers
- Save the class

#### 3. Results Management:
- Go to "Results & Class Management"
- Select a class from the grid
- Enter subject and total marks
- Input individual student marks
- Generate results with analytics

---

## 🔒 Security Notes

### Database Security:
- Use strong passwords for PostgreSQL
- Consider creating a dedicated database user
- Don't commit `.env` files to version control

### Application Security:
- Passwords are hashed using SHA-256
- Database uses parameterized queries
- Session management through Streamlit

---

## 🆘 Getting Help

### Common Commands:
```bash
# Check Python version
python --version

# Check PostgreSQL status
# Windows: 
net start postgresql-x64-13

# Mac:
brew services list | grep postgresql

# Linux:
sudo systemctl status postgresql

# Reset database (if needed)
dropdb class_manager
createdb class_manager
```

### Logs and Debugging:
- Streamlit logs appear in the terminal
- Database errors are shown in the application
- Check browser console for client-side issues

---

## 📈 Performance Optimization

### For Better Performance:
- Use SSD storage for PostgreSQL
- Ensure adequate RAM (4GB+ recommended)
- Close unnecessary browser tabs
- Use latest Chrome/Firefox/Edge browsers

### Database Optimization:
- Regular database maintenance
- Consider indexing for large datasets
- Monitor query performance

---

## 🔄 Updates and Maintenance

### Updating the Application:
1. Download new files
2. Replace existing files (backup first)
3. Update dependencies: `pip install -r local_requirements.txt`
4. Restart the application

### Database Backups:
```bash
# Create backup
pg_dump -U postgres class_manager > backup.sql

# Restore backup
psql -U postgres class_manager < backup.sql
```

---

## ✅ Success Checklist

After setup, verify these work:
- [ ] Application loads at http://localhost:8501
- [ ] Can create new user account
- [ ] Can login successfully
- [ ] Dashboard shows without errors
- [ ] Can create a new class
- [ ] Can add students to class
- [ ] Can generate results
- [ ] Charts display properly

---

**🎉 Congratulations! Your Class Manager application is now running locally.**

For additional support, refer to the detailed README.md file or check the troubleshooting section above.