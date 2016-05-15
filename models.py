from google.appengine.ext import ndb


class Film(ndb.Model):
    ime_filma = ndb.StringProperty()
    ocena_filma = ndb.IntegerProperty()
    slika_filma= ndb.TextProperty()