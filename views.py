
import compositor
from flask import Blueprint, request, redirect, render_template, url_for
from flask.ext.mongoengine.wtf import model_form
from flask.views import MethodView
from moonmemews.models import Texture
from moonmemews import app
import os
from werkzeug import secure_filename

textures = Blueprint('textures', __name__, template_folder='templates')

def allowed_texture_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in app.config['TEXTURE_EXTENSIONS']

class ListView(MethodView):

	form = model_form(Texture, exclude=['filename','created_at'])

	def get_context(self):
		form = self.form(request.form)
		context = {
			'form': form
		}
		return context

	def get(self):
		textures = Texture.objects.all()
		form = self.get_context()['form']
		return render_template('textures.html', textures=textures, form=form)

	def post(self):
		form = self.form(request.form)
		file = request.files['texture_file']
		if form.validate() and file and allowed_texture_file(file.filename):
			filename = secure_filename(file.filename)
			filepath = os.path.join(app.config['TEXTURE_DIR'], filename)
			file.save(filepath)

			compositor.uvpass(
				filepath,
				os.path.join(app.config['BITS_DIR'], 'Flag_UV_Pass_New_RGBA_Fixed_Cropped.png'),
				os.path.join(app.config['TEMP_DIR'], filename))

			compositor.compositeMoonMeme(
				os.path.join(app.config['BITS_DIR'], 'background.jpg'),
				os.path.join(app.config['TEMP_DIR'], filename),
				os.path.join(app.config['BITS_DIR'], 'diffuse.png'),
				os.path.join(app.config['COMPOSITION_DIR'], filename))

			texture = Texture()
			form.populate_obj(texture)
			texture.filename = filename
			texture.save()

			return redirect(url_for('textures.detail', slug=texture.slug))
		return redirect(url_for('textures.list'))

class DetailView(MethodView):

	def get(self, slug):
		texture = Texture.objects.get_or_404(slug=slug)
		return render_template('texture.html', texture=texture)

textures.add_url_rule('/texture', view_func=ListView.as_view('list'))
textures.add_url_rule('/texture/<slug>', view_func=DetailView.as_view('detail'))
