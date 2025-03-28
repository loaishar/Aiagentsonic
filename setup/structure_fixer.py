#!/usr/bin/env python3
"""
OpenManus Directory Structure Fix Script

This script checks and fixes the directory structure of the OpenManus project.
It creates missing directories and files if needed.
"""

import os
import sys
from pathlib import Path


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print a header with formatting."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}\n{text}\n{'='*80}{Colors.ENDC}")


def print_status(text, status, is_error=False):
    """Print a status message."""
    status_color = Colors.FAIL if is_error else Colors.GREEN
    print(f"{status_color}{status}{Colors.ENDC} {text}")


def check_create_dir(directory):
    """Check if a directory exists and create it if not."""
    path = Path(directory)
    if path.exists() and path.is_dir():
        print_status(f"Directory {directory} exists", "✓")
        return True
    else:
        try:
            path.mkdir(parents=True, exist_ok=True)
            print_status(f"Created directory {directory}", "✓")
            return True
        except Exception as e:
            print_status(f"Failed to create directory {directory}: {e}", "✗", True)
            return False


def check_file_exists(file_path):
    """Check if a file exists."""
    path = Path(file_path)
    if path.exists() and path.is_file():
        print_status(f"File {file_path} exists", "✓")
        return True
    else:
        print_status(f"File {file_path} is missing", "✗", True)
        return False


def ensure_essential_files():
    """Check and create essential OpenManus files if missing."""
    essential_dirs = [
        "app",
        "app/agent",
        "app/tool",
        "app/prompt",
        "app/config",
        "app/flow",
        "app/sandbox",
        "config",
        "workspace",
        "logs"
    ]
    
    essential_files = [
        "main.py",
        "app/__init__.py",
        "app/agent/__init__.py",
        "app/tool/__init__.py",
        "config/config.toml"
    ]
    
    # Check and create essential directories
    print_header("Checking Essential Directories")
    all_dirs_ok = True
    for directory in essential_dirs:
        if not check_create_dir(directory):
            all_dirs_ok = False
    
    # Check essential files
    print_header("Checking Essential Files")
    all_files_ok = True
    for file_path in essential_files:
        if not check_file_exists(file_path):
            all_files_ok = False
    
    return all_dirs_ok and all_files_ok


def fix_init_files():
    """Create missing __init__.py files."""
    print_header("Fixing __init__.py Files")
    
    # Find all directories
    dirs_to_check = []
    root_dir = Path("app")
    for path in root_dir.glob("**/*"):
        if path.is_dir() and not path.name.startswith("__"):
            dirs_to_check.append(path)
    
    # Check and create __init__.py in each directory
    for directory in dirs_to_check:
        init_file = directory / "__init__.py"
        if not init_file.exists():
            try:
                with open(init_file, "w") as f:
                    f.write("# Auto-generated __init__.py file\n")
                print_status(f"Created {init_file}", "✓")
            except Exception as e:
                print_status(f"Failed to create {init_file}: {e}", "✗", True)


def check_import_paths():
    """Check for common import path issues."""
    print_header("Checking Import Paths")
    
    # List of files to check
    files_to_check = []
    for ext in [".py"]:
        for path in Path(".").rglob(f"*{ext}"):
            if not str(path).startswith(("__pycache__", ".git", ".venv", "venv")):
                files_to_check.append(path)
    
    # Common import issues to look for
    import_issues = {
        "from openmanus.": "from app.",
        "import openmanus.": "import app.",
        "openmanus.agent.": "app.agent.",
        "openmanus.tool.": "app.tool."
    }
    
    files_with_issues = []
    for file_path in files_to_check:
        if file_path.is_file():
            try:
                content = file_path.read_text()
                has_issues = False
                
                for issue, replacement in import_issues.items():
                    if issue in content:
                        has_issues = True
                        print_status(f"Found '{issue}' in {file_path} - should be '{replacement}'", "⚠", True)
                
                if has_issues:
                    files_with_issues.append(file_path)
            except Exception as e:
                print_status(f"Error reading {file_path}: {e}", "✗", True)
    
    if files_with_issues:
        print(f"\n{Colors.WARNING}Found import issues in {len(files_with_issues)} files.{Colors.ENDC}")
        print(f"{Colors.WARNING}You may need to update import statements to use 'app.' instead of 'openmanus.'{Colors.ENDC}")
    else:
        print(f"\n{Colors.GREEN}No import path issues found.{Colors.ENDC}")
    
    return files_with_issues


def main():
    """Main function."""
    print_header("OpenManus Directory Structure Fix Tool")
    
    dirs_and_files_ok = ensure_essential_files()
    fix_init_files()
    files_with_issues = check_import_paths()
    
    # Summary
    print_header("Summary")
    if dirs_and_files_ok and not files_with_issues:
        print(f"{Colors.GREEN}Directory structure looks good! 🎉{Colors.ENDC}")
        print("All essential directories and files are in place.")
    else:
        print(f"{Colors.WARNING}There are some issues with your directory structure.{Colors.ENDC}")
        print("Please check the messages above and fix the identified issues.")
    
    print("\nAdditional steps you may need to take:")
    print("1. Make sure your config.toml file is properly configured with your API key")
    print("2. Run 'python verify_installation.py' to check the installation")
    print("3. If browser functionality is not working, follow the fix guide")


if __name__ == "__main__":
    main()
