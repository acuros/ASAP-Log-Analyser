import datetime, re
from django.core.urlresolvers import resolve

class ActivityData(object):
    def __init__(self, parsed_dict):
        self.parsed_dict = parsed_dict
        self.key = parsed_dict[1]
        self.value = parsed_dict[2]

    def is_root_element(self):
        return self.parsed_dict[0] == ''

    def has_children(self):
        return self.value == ''

class LogParser(object):
    def __init__(self, log):
        self.log = log

    def get_activity_time(self):
        return datetime.datetime.strptime(log.split('\n')[0], '%Y-%m-%d %H:%M:%S.%f')

    def get_activity_info(self):
        activity_info = dict()
        activity_data_list = self.get_activity_data_list()
        root_key = ''
        for activity_data in activity_data_list:
            if activity_data.is_root_element():
                root_key = activity_data.key
                if activity_data.has_children():
                    activity_info[activity_data.key] = dict()
                else:
                    activity_info[activity_data.key] = activity_data.value
            else:
                activity_info[root_key][activity_data.key] = activity_data.value
        return activity_info

    def get_activity_data_list(self):
        data = log[log.find('\n')+1:]
        return [ActivityData(parsed_dict) for parsed_dict in re.findall(r'(\t*)([a-zA-Z_ ]+) : *(.+)*\n?', data)]


    @classmethod
    def get_requested_view_name(cls, activity_info):
        uri = activity_info['META']['REQUEST_URI']
        return re.match(r"<class '.*\.(\w+)'", str(resolve(uri).func.__self__)).groups()[0]


class Activity(object):
    def __init__(self, log):
        log_parser = LogParser(log)
        self.time = log_parser.get_activity_time()
        activity_info = log_parser.get_activity_info()
        for key, value in activity_info.iteritems():
            setattr(self, key, value)

        
f = file('log.txt', 'r')
logdata = f.read().split('====================================================================================================\n')[1:]
activities = []
for log in logdata:
    activities.append(Activity(log))
f.close()
