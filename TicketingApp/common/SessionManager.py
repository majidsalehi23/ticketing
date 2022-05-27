import bcrypt
import hashlib


class Session:

    def __init__(self, username, sessionKey, cookie, IP, agent):
        self.username = username
        self.sessionKey = sessionKey
        self.cookie = cookie
        self.IP = IP
        self.agent = agent

    def getCookie(self):
        return self.cookie


class SessionManager:

    userSessions = {}

    def __init__(self):
        pass

    @staticmethod
    def getCurrentUserName():
        from Middleware import GlobalRequestMiddleware
        currentRequest = GlobalRequestMiddleware.getCurrentRequest()
        username = str(currentRequest.COOKIES.get('username'))
        cookie = str(currentRequest.COOKIES.get('session_cookie'))
        if SessionManager.sessionValid(username, cookie):
            return username
        else:
            return None

    @staticmethod
    def createUserSession(username, IP, agent):
        if username in SessionManager.userSessions:
            print("Session Already Exists")
        cookie = SessionManager.generateCookie()
        sessionKey = SessionManager.generateSessionKey()
        session = Session(username, sessionKey, cookie, IP, agent)
        SessionManager.setUserSession(username, session)

    @staticmethod
    def sessionValid(username, cookie):
        userSession = SessionManager.getUserSession(username)
        if userSession and userSession.getCookie() == cookie:
            return True
        else:
            return False

    @staticmethod
    def getUserCookie(username):
        userSession = SessionManager.getUserSession(username)
        return userSession.cookie

    @staticmethod
    def generateCookie():
        return hashlib.md5(SessionManager.generateNewSalt()).hexdigest()

    @staticmethod
    def generateSessionKey():
        return hashlib.md5(SessionManager.generateNewSalt()).hexdigest()

    @staticmethod
    def generateNewSalt():
        salt = bcrypt.gensalt()
        return salt

    @staticmethod
    def setUserSession(username, userSession):
        if username not in SessionManager.userSessions:
            SessionManager.userSessions[username] = userSession

    @staticmethod
    def getUserSession(username):
        if username in SessionManager.userSessions:
            return SessionManager.userSessions[username]
        else:
            return None
