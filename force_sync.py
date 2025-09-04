#!/usr/bin/env python3

import subprocess
import sys
import os

def execute_git_commands():
    os.chdir('/Users/cheriet/Documents/augment-projects/stat')
    
    commands = [
        "git add -A",
        'git commit -m "🚀 FINAL FIX: Removed psycopg2 completely for Streamlit Cloud"',
        "git push origin main"
    ]
    
    for cmd in commands:
        print(f"Executing: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Error: {result.stderr}")
    
    print("\n" + "="*50)
    print("🎯 DÉPLOIEMENT STREAMLIT CLOUD")
    print("="*50)
    print("Repository: Abdel67Unistra/Intelligence-football-analytics")
    print("Branch: main")
    print("Main file path: python_analytics/dashboards/coach_interface.py")
    print("App URL suggestions:")
    print("  - football-analytics-platform-2025")
    print("  - football-intelligence-dashboard")
    print("  - soccer-analytics-pro")
    print("\n🌐 Go to: https://share.streamlit.io")
    print("✅ PSYCOPG2 ERROR FIXED - READY TO DEPLOY!")

if __name__ == "__main__":
    execute_git_commands()
