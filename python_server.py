# -*- coding: utf-8 -*-
'''
Based on https://github.com/tornadoweb/tornado/blob/master/demos/blog/blog.py
'''

# Importing all stuff from tornado
import tornado.httpserver
import tornado.ioloop 
import tornado.options
import tornado.web

# Importing everything else required...
import os.path

# NoSQL config
from pymongo import MongoClient
# Define port
from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

# Tornado application
class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			tornado.web.url(r"/",IndexHandler, name="home"),
			tornado.web.url(r"/cv", CVHandler, name="cv"),
			tornado.web.url(r"/cvpdf", CVDownloadHandler, name="cv_download"),
		]
		settings = {
			'title': "CV de J. Perron",
			'template_path': os.path.join(os.path.dirname(__file__), "templates"),
			'static_path': os.path.join(os.path.dirname(__file__), "static"),
			'autoreload' : True,
			'default_handler_class': tornado.web.RedirectHandler, #Handle 404 very efficiently !
			'default_handler_args': {"url":"/"},		
		}
		super(Application, self).__init__(handlers, **settings)
		self.client = MongoClient()
		self.database = self.client['monsite']
		
# Generates responses
class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html")
	
class CVHandler(tornado.web.RequestHandler):
	def get(self):
		db=self.application.database
		competences = []
		for skill in db["skills"].find():
			competences.append([str(skill['nom']),str(skill['niveau'])])
		
		experiences = []
		for experience in db["experiences"].find():
			experiences.append([
				experience['Titre'].encode('utf-8'),
				experience['Employeur'].encode('utf-8'),
				experience['Date'].encode('utf-8'),
				experience['Lieu'].encode('utf-8'),
				experience[u'Résumé'].encode('utf-8'),
				experience['Mots-clef'].encode('utf-8'),
			])
		experiences.reverse()
						
		self.render("cv.html",competences=competences,experiences=experiences)

class CVDownloadHandler(tornado.web.StaticFileHandler):
	def get(self):
		filename = 'PERRON_CV.pdf'
		with open(filename,'rb') as f:
			self.set_header("Content-Type","application/pdf; charset='utf-8'")
			self.set_header("Content-Disposition","attachment; filename=perron_cv.pdf")
			
			self.write(f.read())
			
def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
	
if __name__ == "__main__":
	main()	
