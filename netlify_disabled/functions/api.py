import sys
import os

# Add the backend directory to Python path
sys.path.append('/opt/build/repo/backend')

# Set environment variables
os.environ.setdefault('OPENROUTER_API_KEY', '')
os.environ.setdefault('OPENROUTER_MODEL', 'deepseek/deepseek-chat-v3-0324:free')
os.environ.setdefault('OPENROUTER_SITE_URL', 'https://fullstack-aibot.netlify.app')
os.environ.setdefault('SECRET_KEY', 'netlify-secret-key-change-this')

from main import app

def handler(event, context):
    """Netlify function handler"""
    from mangum import Mangum
    
    asgi_handler = Mangum(app)
    return asgi_handler(event, context)
