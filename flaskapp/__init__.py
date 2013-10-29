from flask import Flask, redirect, render_template, request, url_for
import os
from werkzeug import secure_filename


assert 'SECRET_KEY' in os.environ

TEXTURE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/textures'
TEMP_DIR = os.path.dirname(os.path.abspath(__file__)) + '/temp'
BITS_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/bits'
COMPOSITION_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/compositions'
TEXTURE_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

app = Flask(__name__)
app.debug = True

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

app.config['TEXTURE_DIR'] = TEXTURE_DIR
app.config['BITS_DIR'] = BITS_DIR
app.config['TEMP_DIR'] = TEMP_DIR
app.config['COMPOSITION_DIR'] = COMPOSITION_DIR
app.config['TEXTURE_EXTENSIONS'] = TEXTURE_EXTENSIONS

for key in ['MONGODB_HOST', 'MONGODB_PORT', 'MONGODB_DB', 'MONGODB_USERNAME', 'MONGODB_PASSWORD']:
	if key in os.environ:
		app.config[key] = os.environ[key]

def register_blueprints():
	# Prevent circular imports.
	from views import textures
	app.register_blueprint(textures)
register_blueprints()

@app.route('/')
def index():
	return 'Hello world!'

