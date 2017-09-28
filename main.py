#!/usr/bin/env python
import os
import jinja2
import webapp2

from models import Sporocilo

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")


class RezultatHandler(BaseHandler):
    def post( self ):
        rezultat = self.request.get("vnos")

        sporocilo = Sporocilo( vnos=rezultat )
        sporocilo.put()
        return self.write(rezultat)

class ShowMessagesHandler( BaseHandler ):
    def get( self ):
        messages = Sporocilo.query( Sporocilo.deleted == False).fetch()
        params = {
            "messages": messages
        }
        return self.render_template( "messages.html", params=params )

class ShowSingleMessage( BaseHandler ):
    def get( self, message_id ):
        message = Sporocilo.get_by_id( int( message_id ) )
        params = {
            "message": message
        }
        return self.render_template( "message.html", params=params )


class EditMessageHandler( BaseHandler ):
    def get (self, message_id):
        message =Sporocilo.get_by_id( int( message_id))
        params = {
            "message": message
        }
        return self.render_template( "edit_message.html", params=params )
    def post(self, message_id):
        message = Sporocilo.get_by_id( int(message_id))
        message_content = self.request.get( "message_content" )
        message.vnos = message_content
        message.put()
        return self.redirect_to( "messages" )

class DeleteMessageHandler( BaseHandler ):
    def get( self, message_id ):
        message = Sporocilo.get_by_id( int( message_id ) )

        params ={
            "message":message
        }

        return self.render_template( "delete_message.html", params=params )

    def post(self, message_id):
        message = Sporocilo.get_by_id( int(message_id))
        #message.key.delete()
        message.deleted = True
        message.put()
        return self.redirect_to( "messages" )

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/rezultat', RezultatHandler),
    webapp2.Route('/messages', ShowMessagesHandler, name="messages"),
    webapp2.Route('/message/<message_id:\d+>', ShowSingleMessage),
    webapp2.Route('/edit/<message_id:\d+>', EditMessageHandler),
    webapp2.Route('/delete/<message_id:\d+>', DeleteMessageHandler),
], debug=True)