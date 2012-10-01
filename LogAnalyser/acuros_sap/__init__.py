#-*-coding:utf8-*-
import string, random, json, django, hashlib
from django.http import HttpResponse
from django.contrib.auth.models import User
from acuros_sap.exceptions import NoParameterError, UnsupportedRequestMethodError, WrongFormatError, NotAuthenticatedUserError, InvalidParameterError
from acuros_sap.logger import Logger


_LOWERCASE = ''.join(string.ascii_lowercase)
_USERNAME = ''.join([
    string.ascii_lowercase,
    string.ascii_uppercase,
    string.digits,
])
_PASSWORD = ''.join([
    string.ascii_lowercase,
    string.ascii_uppercase,
    string.digits,
    filter(lambda x: x != '\\', string.punctuation),
])

class ASAP(object):
    response = None
    login_required = False

    def __init__(self, request, *args):
        self.request = request
        exception = None
        traced_back = '' 
        process_method_name = 'process_%s_request'%self.request.method.lower()
        self.set_trace_hash()
        try:
            self.version = self.get_parameter('version', is_required=False, default='1.0.0')
            if self.login_required:
                self.get_user()
            if hasattr(self, process_method_name) and callable(getattr(self, process_method_name)):
                result = getattr(self, process_method_name)(*args) or dict()
            else:
                raise UnsupportedRequestMethodError("The method '%s' is not valid method for this request."%(self.request.method))
        except Exception, exception:
            self.return_dict = {'status':{'code':str(exception.__class__.__name__), 'reason':unicode(exception)}}
            import traceback
            traced_back = traceback.format_exc()
        else:
            self.return_dict = {'status':{'code':'OK', 'reason':'OK'}}
            self.return_dict.update(result)
        
        Logger(self.return_dict, exception, traced_back).log()
        self.response = self.get_json_response()

    def set_trace_hash(self):
        self.request.session['trace_hash'] = self.request.session.get('trace_hash', self.get_random_hash())
    
    def get_file_parameter (self, parameter_name, default=None, is_required=True):
        return self.get_parameter(parameter_name, parameter_pool=self.request.FILES, default=default, is_required=is_required, type=None)
    
    def get_post_parameter (self, parameter_name, default="", is_required=True, type=unicode):
        return self.get_parameter(parameter_name, parameter_pool=self.request.POST, default=default, is_required=is_required, type=type)

    def get_get_parameter (self, parameter_name, default="", is_required=True, type=unicode):
        return self.get_parameter(parameter_name, parameter_pool=self.request.GET, default=default, is_required=is_required, type=type)

    def get_parameter(self, parameter_name, parameter_pool=None, default="", is_required=True, type=None):
        def get_parsed_parameter():
            if type == None:
                return parameter
            try:
                return type(parameter)
            except Exception:
                raise InvalidParameterError(u"Type of %s must be %s, not %s"%(parameter_name, str(type), str(type(parameter))))
        if parameter_pool == None:
            parameter_pool = self.request.REQUEST
        parameter = parameter_pool.get(parameter_name, None)
        if parameter == None:
            if is_required:
                raise NoParameterError(parameter_name)
            else:
                return default
        return get_parsed_parameter()

    def get_object_from_json_string(self, parameter_name, json_string):
        try:
            return json.loads(json_string)
        except Exception:
            raise WrongFormatError(parameter_name)

    def get_json_response(self):
        json_object = json.dumps(self.return_dict)
        response = HttpResponse(json_object, mimetype='application/json')
        response['Cache-Control'] = 'no-cache'
        return response
    
    def get_user (self, user=None):
        if user:
            return user
        username = self.get_parameter('username')
        id = self.get_parameter('uid')
        try:
            return User.objects.get(id=id, username=username)
        except User.DoesNotExist:
            raise NotAuthenticatedUserError("Username or uid is invalid")

    def get_random_hash(self):
        return hashlib.sha256(''.join(random.sample(string.lowercase+string.uppercase+string.punctuation+string.whitespace+string.digits, 100))).hexdigest()

    @classmethod
    def link_to_view(cl ,request, *args):
        return cl(request, *args).response


def generate_username_and_password():
    USERNAME_LENGTH = 8
    PASSWORD_LENGTH = 10

    username = ''.join([
        ''.join(random.sample(_LOWERCASE, 1)),
        ''.join(random.sample(_USERNAME, USERNAME_LENGTH - 1)),
    ])
    password = ''.join(random.sample(_PASSWORD, PASSWORD_LENGTH))

    return username, password

def http_response_as_json (object_to_be_json):
    json_object = json.dumps(object_to_be_json)
    response = HttpResponse(json_object, mimetype='application/json')
    response['Cache-Control'] = 'no-cache'
    return response


def standardize_phone_number (tmp_phone_number):
    phone_number = filter(lambda x:x in "1234567890+#", tmp_phone_number)
    if len(phone_number) < 10 or len(phone_number) > 15:
        raise WrongFormatError("Phone number is not valid type of phone number")
    return phone_number
