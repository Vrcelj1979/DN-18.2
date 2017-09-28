from google.appengine.ext import ndb

class Sporocilo( ndb.Model ):
    vnos = ndb.StringProperty()
    date = ndb.DateTimeProperty( auto_now_add = True )
    delete = ndb.BooleanProperty( default = False )