#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import cgi
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

# Create database
class BlogPost(db.Model):
	post_title = db.StringProperty(required = True)
	post_content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)


# Create main handler
class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render (self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainPage(Handler):

	def render_index(self, post_title="", post_content="", error=""):
		BlogPosts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC")

		self.render("index.html", post_title=post_title,
			post_content=post_content, error=error, BlogPosts=BlogPosts)

	def get(self):
		self.render_index()

	def post(self):
		post_title = self.request.get("post_title")
		post_content = self.request.get("post_content")

		if post_title and post_content:
			blog_post = BlogPost(post_title=post_title, post_content=post_content)
			blog_post.put()

			self.redirect("/")
		else:
			error = "A blog post requires both a title and content."
			self.render_index(post_title, post_content, error)

# Paths
app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
