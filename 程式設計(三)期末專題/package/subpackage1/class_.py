
class Response():
    def __init__(self, status_code=None, message='', result=None):
        self.status_code = status_code
        self.message = message
        self.result = result
