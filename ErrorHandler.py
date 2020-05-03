from bson.errors import BSONError

class APIError(Exception):
    statusCode = 500

class Error404(APIError):
    statusCode = 404

def exception_info(status, message, error_code):
    info = {
        "status" : status,
        "message" : message
    }
    return info, error_code

def error_handler(fn):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except APIError as e:
            print(e)
            info = exception_info('error', str(e), e.statusCode)
            return info
        except BSONError as e:
            print(e)
            info = exception_info('error', str(e), 500)
            return info
    wrapper.__name__ = fn.__name__
    return wrapper