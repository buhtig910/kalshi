#!/usr/bin/env python3
"""
Setup script for Kalshi Data Extractor
Installs dependencies and provides usage instructions
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages from requirements.txt"""
    print("🔧 Installing Kalshi Data Extractor dependencies...")
    print("=" * 50)
    
    try:
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("\n✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error installing dependencies: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    return True

def main():
    """Main setup function"""
    print("🎯 Kalshi Data Extractor Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    
    # Install requirements
    if install_requirements():
        print("\n🚀 Setup complete! You can now run:")
        print("   python kalshi_gui.py          # For GUI interface")
        print("   python run_kalshi_extraction.py  # For command line")
        print("\n📚 Available files:")
        print("   - kalshi_gui.py: Easy-to-use GUI interface")
        print("   - run_kalshi_extraction.py: Command line extraction")
        print("   - kalshi_top_volumes.py: Core extraction logic")
        print("   - kalshi_api_client.py: API client library")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
