from flask import Flask, redirect, render_template, request, url_for
import os
from werkzeug import secure_filename

assert 'MONGODB_DATABASE' in os.environ
assert 'MONGODB_SECRET' in os.environ

TEXTURE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/textures'
TEMP_DIR = os.path.dirname(os.path.abspath(__file__)) + '/temp'
BITS_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/bits'
COMPOSITION_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/compositions'
TEXTURE_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

app = Flask(__name__)
app.debug = True
app.config['TEXTURE_DIR'] = TEXTURE_DIR
app.config['BITS_DIR'] = BITS_DIR
app.config['TEMP_DIR'] = TEMP_DIR
app.config['COMPOSITION_DIR'] = COMPOSITION_DIR
app.config['TEXTURE_EXTENSIONS'] = TEXTURE_EXTENSIONS
app.config['MONGODB_SETTINGS'] = {'DB': os.environ['MONGODB_DATABASE']}
app.config['SECRET_KEY'] = os.environ['MONGODB_SECRET']

def register_blueprints(app):
	# Prevents circular imports.
	from moonmemews.views import textures
	app.register_blueprint(textures)

register_blueprints(app)

@app.route('/')
def index():
	return 'Hello world!'

if __name__ == '__main__':
	app.run()

