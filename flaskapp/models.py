
import datetime
from flask import url_for
from flask.ext.mongoengine import MongoEngine
from flaskapp import app

db = MongoEngine(app)

class Texture(db.Document):
	name = db.StringField(max_length=255, required=True)
	created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
	filename = db.StringField(max_length=255, required=True)
	slug = db.StringField(max_length=255, required=True)

	def __unicode__(self):
		return self.name

	meta = {
		'allow_inheritance': True,
		'indexes': ['-created_at', 'slug'],
		'ordering': ['-created_at']
	}
