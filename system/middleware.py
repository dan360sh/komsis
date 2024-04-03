import threading

from django.contrib.sessions.backends.db import SessionStore
from django.utils.deprecation import MiddlewareMixin

REQUEST_OBJECT = threading.local()


class SessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            session = request.session.session_key
        except AttributeError:
            session = SessionStore()
            session.save()
            request.session = session


class CreateOrder(MiddlewareMixin):
    def process_request(self, request):
        REQUEST_OBJECT.request = request
        if request.get_full_path() == "/createorder/" and \
                not request.user.is_authenticated:
            request.session['createorder'] = True
            request.session.save()
