#!/usr/bin/env python3
"""
OpenManus Project Cleanup Script

This script identifies and removes duplicated files and directories between
the root directory and the OpenManus directory.
"""

import os
import shutil
import sys
from pathlib import Path

def print_header(message):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f" {message}")
    print("=" * 80)

def print_success(message):
    """Print a success message."""
    print(f"✅ {message}")

def print_warning(message):
    """Print a warning message."""
    print(f"⚠️  {message}")

def print_error(message):
    """Print an error message."""
    print(f"❌ {message}")

def remove_directory(path):
    """Remove a directory and all its contents."""
    try:
        if os.path.exists(path):
            shutil.rmtree(path)
            print_success(f"Removed directory: {path}")
        else:
            print_warning(f"Directory not found: {path}")
    except Exception as e:
        print_error(f"Failed to remove directory {path}: {str(e)}")

def remove_file(path):
    """Remove a file."""
    try:
        if os.path.exists(path):
            os.remove(path)
            print_success(f"Removed file: {path}")
        else:
            print_warning(f"File not found: {path}")
    except Exception as e:
        print_error(f"Failed to remove file {path}: {str(e)}")

def cleanup_project():
    """Clean up duplicated files and directories."""
    print_header("OpenManus Project Cleanup")
    
    # Get the current working directory
    cwd = os.getcwd()
    print(f"Current working directory: {cwd}")
    
    # List of directories to remove
    directories_to_remove = [
        "app",          # Duplicated app directory
        "config",       # Duplicated config directory
        ".vscode"       # VSCode configuration
    ]
    
    # List of files to remove
    files_to_remove = [
        "setup/verify_installation.py"  # Duplicated verification script
    ]
    
    # Remove directories
    print_header("Removing Duplicated Directories")
    for directory in directories_to_remove:
        remove_directory(directory)
    
    # Remove files
    print_header("Removing Duplicated Files")
    for file in files_to_remove:
        remove_file(file)
    
    print_header("Cleanup Summary")
    print("The following items were cleaned up:")
    print("1. app directory (duplicated from OpenManus/app)")
    print("2. config directory (duplicated from OpenManus/config)")
    print("3. .vscode directory (configuration for OpenManus)")
    print("4. setup/verify_installation.py (duplicated from OpenManus/verify_installation.py)")
    
    print("\nThe OpenManus directory now contains the complete project without duplications.")

if __name__ == "__main__":
    # Ask for confirmation before proceeding
    print("This script will remove duplicated files and directories in the project.")
    print("Make sure you have a backup before proceeding.")
    
    response = input("Do you want to continue? (y/n): ")
    if response.lower() == 'y':
        cleanup_project()
    else:
        print("Cleanup cancelled.")