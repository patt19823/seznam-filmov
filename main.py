#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Film


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")


class VnesiFilmHandler(BaseHandler):
    def post(self):
        ime_filma = self.request.get("ime_filma")
        ocena_filma = int(self.request.get("ocena_filma"))
        slika_filma = self.request.get("slika_filma")

        vnos_filma = Film(ime_filma=ime_filma, ocena_filma=ocena_filma, slika_filma=slika_filma)
        vnos_filma.put()

        view_vars = { "ime_filma": ime_filma,
                      "ocena_filma": ocena_filma,
                      "slika_filma": slika_filma}

        return self.render_template("vnosuspesen.html", view_vars)

class SeznamdFilmovHandler(BaseHandler):
    def get(self):
        vsi_filmi = Film.query().order().fetch()

        view_vars = {
            "vsi_filmi": vsi_filmi,
        }

        return self.render_template("seznamfilmov.html", view_vars)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/vnesifilm', VnesiFilmHandler),
    webapp2.Route('/seznamfilmov', SeznamdFilmovHandler),

], debug=True)
