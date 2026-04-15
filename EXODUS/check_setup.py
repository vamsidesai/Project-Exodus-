import shutil
import sys
import os

def check_tool(name, check_cmd=None):
    found = shutil.which(name) is not None
    status = "✅ FOUND" if found else "❌ MISSING"
    print(f"{name.ljust(10)}: {status}")
    return found

def main():
    print("--- EXODUS ENVIRONMENT CHECK ---\n")
    
    git = check_tool("git")
    python = check_tool("python")
    ollama = check_tool("ollama")
    
    print("\n--- DIAGNOSIS ---")
    if not git:
        print("1. Install Git: https://git-scm.com/download/win")
    if not python:
        print("2. Install Python: https://www.python.org/downloads/ (Check 'Add to PATH')")
    if not ollama:
        print("3. Install Ollama: https://ollama.com")
        
    if git and python and ollama:
        print("All systems go! Run 'python interfaces/terminal.py'")
    else:
        print("\nPlease install missing tools and restart your terminal.")
        
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
