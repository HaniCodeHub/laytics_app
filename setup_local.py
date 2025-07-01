#!/usr/bin/env python3
"""
Local setup script for Class Manager Application
This script helps set up the environment and verify the installation
"""

import os
import sys
import subprocess
import psycopg2
from psycopg2 import OperationalError

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} is compatible")
    return True

def check_postgresql():
    """Check if PostgreSQL is installed and accessible"""
    print("\n🐘 Checking PostgreSQL...")
    try:
        # Try to connect to PostgreSQL
        # This will use default connection (usually to 'postgres' database)
        conn = psycopg2.connect(
            host=os.getenv('PGHOST', 'localhost'),
            user=os.getenv('PGUSER', 'postgres'),
            password=os.getenv('PGPASSWORD', ''),
            port=os.getenv('PGPORT', 5432),
            dbname='postgres'  # Connect to default postgres database first
        )
        conn.close()
        print("✅ PostgreSQL is accessible")
        return True
    except OperationalError as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        print("💡 Make sure PostgreSQL is installed and running")
        print("💡 Check your environment variables: PGHOST, PGUSER, PGPASSWORD, PGPORT")
        return False

def install_requirements():
    """Install Python requirements"""
    print("\n📦 Installing Python packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "local_requirements.txt"])
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def create_database():
    """Create the application database if it doesn't exist"""
    print("\n🗄️  Setting up database...")
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            host=os.getenv('PGHOST', 'localhost'),
            user=os.getenv('PGUSER', 'postgres'),
            password=os.getenv('PGPASSWORD', ''),
            port=os.getenv('PGPORT', 5432),
            dbname='postgres'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'class_manager'")
        if cursor.fetchone():
            print("✅ Database 'class_manager' already exists")
        else:
            # Create database
            cursor.execute("CREATE DATABASE class_manager")
            print("✅ Database 'class_manager' created successfully")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def create_streamlit_config():
    """Create Streamlit configuration directory and file"""
    print("\n⚙️  Setting up Streamlit configuration...")
    
    # Create .streamlit directory
    os.makedirs('.streamlit', exist_ok=True)
    
    # Create config.toml
    config_content = """[server]
headless = true
address = "0.0.0.0"
port = 8501

[theme]
base = "dark"
"""
    
    with open('.streamlit/config.toml', 'w') as f:
        f.write(config_content)
    
    print("✅ Streamlit configuration created")

def create_env_template():
    """Create environment variable template"""
    print("\n🔧 Creating environment template...")
    
    env_template = """# Copy this file to .env and fill in your PostgreSQL credentials
# Or set these as environment variables

PGHOST=localhost
PGDATABASE=class_manager
PGUSER=postgres
PGPASSWORD=your_postgresql_password_here
PGPORT=5432
"""
    
    with open('.env.template', 'w') as f:
        f.write(env_template)
    
    print("✅ Environment template created (.env.template)")
    print("💡 Copy .env.template to .env and update with your credentials")

def verify_installation():
    """Verify that the application can start"""
    print("\n🔍 Verifying installation...")
    try:
        # Import main modules to check for import errors
        import streamlit
        import psycopg2
        import pandas
        import matplotlib
        import seaborn
        import plotly
        
        print("✅ All required modules can be imported")
        
        # Test database connection with application database
        conn = psycopg2.connect(
            host=os.getenv('PGHOST', 'localhost'),
            database=os.getenv('PGDATABASE', 'class_manager'),
            user=os.getenv('PGUSER', 'postgres'),
            password=os.getenv('PGPASSWORD', ''),
            port=os.getenv('PGPORT', 5432)
        )
        conn.close()
        print("✅ Database connection successful")
        
        return True
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Setup Complete!")
    print("\n📋 Next Steps:")
    print("1. Set your PostgreSQL credentials in environment variables or .env file")
    print("2. Run the application with: streamlit run main.py")
    print("3. Open your browser to: http://localhost:8501")
    print("\n🔧 Environment Variables Needed:")
    print("   PGHOST=localhost")
    print("   PGDATABASE=class_manager")
    print("   PGUSER=postgres")
    print("   PGPASSWORD=your_password")
    print("   PGPORT=5432")
    print("\n🆘 If you encounter issues:")
    print("   - Check that PostgreSQL is running")
    print("   - Verify your database credentials")
    print("   - Ensure all environment variables are set")

def main():
    """Main setup function"""
    print("🚀 Class Manager Application - Local Setup")
    print("=" * 50)
    
    steps = [
        ("Checking Python version", check_python_version),
        ("Installing requirements", install_requirements),
        ("Checking PostgreSQL", check_postgresql),
        ("Creating database", create_database),
        ("Setting up Streamlit config", create_streamlit_config),
        ("Creating environment template", create_env_template),
        ("Verifying installation", verify_installation)
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Setup failed at: {step_name}")
            print("Please resolve the issue and run the setup again.")
            return False
    
    print_next_steps()
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Setup completed successfully!")
    else:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)