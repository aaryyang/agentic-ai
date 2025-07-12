# Agentic AI Project Management
# Quick commands for common development tasks

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and show the description."""
    print(f"\n🚀 {description}")
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
        return False
    else:
        print(f"✅ Success: {description}")
        if result.stdout:
            print(result.stdout)
        return True

def main():
    # Ensure we're in the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    print("🤖 Agentic AI Project Manager")
    print("=" * 50)
    
    # Check if virtual environment exists
    venv_path = project_dir / ".venv"
    if not venv_path.exists():
        print("❌ Virtual environment not found. Please run setup.ps1 or setup.bat first.")
        return
    
    # Determine the correct Python executable
    if sys.platform == "win32":
        python_exe = venv_path / "Scripts" / "python.exe"
        pip_exe = venv_path / "Scripts" / "pip.exe"
    else:
        python_exe = venv_path / "bin" / "python"
        pip_exe = venv_path / "bin" / "pip"
    
    # Menu options
    while True:
        print("\nChoose an option:")
        print("1. Start API Server")
        print("2. Run Interactive Chat")
        print("3. Install/Update Dependencies")
        print("4. Format Code")
        print("5. Check Environment")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            cmd = f'"{python_exe}" -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000'
            run_command(cmd, "Starting API Server")
        
        elif choice == "2":
            cmd = f'"{python_exe}" scripts/interactive_chat.py'
            run_command(cmd, "Starting Interactive Chat")
        
        elif choice == "3":
            cmd = f'"{pip_exe}" install -r requirements.txt'
            run_command(cmd, "Installing/Updating Dependencies")
        
        elif choice == "4":
            cmd = f'"{python_exe}" -m black .'
            run_command(cmd, "Formatting Code")
        
        elif choice == "5":
            print(f"\n📊 Environment Status:")
            print(f"Python executable: {python_exe}")
            print(f"Virtual environment: {venv_path}")
            print(f"Working directory: {project_dir}")
            
            # Check if .env exists
            env_file = project_dir / ".env"
            if env_file.exists():
                print("✅ .env file found")
            else:
                print("⚠️  .env file not found (copy from .env.example)")
        
        elif choice == "6":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
