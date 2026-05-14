"""
AI Procurement Scorecard — Django Application
Run with: python manage.py runserver
Then open: http://127.0.0.1:8000/
Admin:     http://127.0.0.1:8000/admin/  (admin / admin123)
"""
import subprocess
import sys

if __name__ == '__main__':
    subprocess.run([sys.executable, 'manage.py', 'runserver'])
