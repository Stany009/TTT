from waitress import serve
from main import app
serve(app, host='0.0.0.0', port=5000, static_url='/static', static_path='static')
