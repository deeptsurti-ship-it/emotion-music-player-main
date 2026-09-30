#!/usr/bin/env python
"""
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emotion_player.settings')
    django.setup()
    
    print("🔧 Setting up the Emotion Player application...")
    
    print("📝 Creating migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    print("🗄️ Applying migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("✅ Setup complete!")
    print("📋 Next steps:")
    print("1. Run: python manage.py createsuperuser")
    print("2. Run: python manage.py runserver")
    print("3. (Optional) Visit: http://127.0.0.1:8000/admin/")
    print("4. Visit: http://127.0.0.1:8000/ to test the emotion detection")


