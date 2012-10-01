import datetime, os, copy, inspect

from django.conf import settings


class Logger(object):
    def __init__ (self, response, exception=None, traced_back=None):
        self.code = response['status']['code']
        self.reason = response['status']['reason']
        self.return_dict = copy.deepcopy(response)
        del self.return_dict['status']
        self.caller = inspect.stack()[1]

        if traced_back != '':
            self.traced_back = 'Traced back :\n%s'%traced_back
        else:
            self.traced_back = ''

        self.log()

    def log (self):
        log_str = self._get_log_str()
        self._write_log_to_file_with_time(log_str)

    def _get_log_str (self):
        request = self.caller[0].f_locals['request']
        meta_info = dict(HTTP_USER_AGENT='', REMOTE_ADDR='', REMOTE_PORT='', REQUEST_METHOD='', REQUEST_URI='')
        for key in meta_info.keys():
            meta_info[key] = request.META.get(key, None)
        logs = ['', 'GET : %s'%self._get_dict_str(request.GET), 'POST : %s'%self._get_dict_str(request.POST), 'COOKIES : %s'%self._get_dict_str(request.COOKIES), 'SESSION : %s'%self._get_dict_str(request.session), 'META : %s'%self._get_dict_str(meta_info), 'Return code : %s'%self.code, 'Reason : %s'%self.reason]
        response_variables_str = self._get_dict_str(self.return_dict)
        logs.append('Response variables : %s'%response_variables_str)
        return '\n'.join(logs)
    
    def _get_caller_function (self):
        filename = self.caller[1].split('/')[-1]
        function_name = self.caller[3]
        return '%s in %s'%(filename, function_name)
    
    def _get_dict_str (self, dictionary):
        dict_str = ['']
        for key, value in dictionary.iteritems():
            dict_str.append('%s : %s'%(key, unicode(value).replace('\n','\n\t\t')))
        return '\n\t'.join(dict_str)

    def _write_log_to_file_with_time (self, log_str):
        filename = os.path.join(settings.PROJECT_PATH, 'log','response_log.txt')
        f = file(filename, 'ab')
        current_time = unicode(datetime.datetime.now().isoformat(' '))
        log_str = unicode(log_str)
        content = ("%s\n%s%s\n%s\n\n"%("="*100, current_time, log_str, self.traced_back)).encode('utf-8')
        f.write(content)
        f.close()
