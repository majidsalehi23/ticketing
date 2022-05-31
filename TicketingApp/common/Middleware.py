import threading
from TicketingApp.urls import publicUrlsString
from TicketingApp.common.SessionManager import SessionManager
from django.shortcuts import redirect


class AuthMiddleware:

    def __init__(self, getResponse):
        self.getResponse = getResponse

    def __call__(self, request):
        if request.path not in publicUrlsString:
            username = str(request.COOKIES.get('username'))
            cookie = str(request.COOKIES.get('session_cookie'))
            sessionValidateResult = SessionManager.sessionValid(username, cookie)
            if not sessionValidateResult:
                return redirect('/TicketingApp/login/')

        response = self.getResponse(request)
        return response


class GlobalRequestMiddleware(object):

    _threadMap = {}

    @classmethod
    def getCurrentRequest(cls):
        return cls._threadMap[threading.get_ident()]

    def __init__(self, getResponse):
        self.getResponse = getResponse

    def process_exception(self, request, exception):
        try:
            del self._threadMap[threading.get_ident()]
        except KeyError:
            pass

    def __call__(self, request):
        self._threadMap[threading.get_ident()] = request
        response = self.getResponse(request)

        try:
            del self._threadMap[threading.get_ident()]
        except KeyError:
            pass

        return response
