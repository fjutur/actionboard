import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

from django.utils import simplejson
from google.appengine.ext import db

class JsonProperty(db.TextProperty):
	def validate(self, value):
		return value

	def get_value_for_datastore(self, model_instance):
		result = super(JsonProperty, self).get_value_for_datastore(model_instance)
		result = simplejson.dumps(result)
		return db.Text(result)

	def make_value_from_datastore(self, value):
		try:
			value = simplejson.loads(str(value))
		except:
			pass

		return super(JsonProperty, self).make_value_from_datastore(value)


class ProjectsBackup(db.Model):
    data = db.StringProperty()

class Backup(webapp.RequestHandler):
  def get(self):
    name = self.request.get('name')
    data = db.get(db.Key.from_path("ProjectsBackup", name)).data;
    self.response.out.write(data);
  
  def put(self):
    name = self.request.get('name')
    backup = ProjectsBackup(key_name=name, data=str(self.request.body))
    backup.put()
    self.response.out.write(" backup: ");

class MainPage(webapp.RequestHandler):
  def get(self):

    template_values = {}
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/backup', Backup)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
