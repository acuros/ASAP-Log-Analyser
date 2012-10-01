import datetime, re
from activityApp.models import *

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
        return datetime.datetime.strptime(self.log.split('\n')[0], '%Y-%m-%d %H:%M:%S.%f')

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
        data = self.log[self.log.find('\n')+1:]
        return [ActivityData(parsed_dict) for parsed_dict in re.findall(r'(\t*)([a-zA-Z_ ]+) : *(.+)*\n?', data)]
        

def parse():
    f = file('log.txt', 'r')
    logdata = f.read().split('====================================================================================================\n')[1:]
    activities = []
    for log in logdata:
        log_parser = LogParser(log)
        
        time = log_parser.get_activity_time()
        activity_data = log_parser.get_activity_info()
        activity_data['time'] = time
        activities.append(activity_data)
    f.close()
       
    for activity_info in activities:
        Activity.load_from_dictionary(activity_info)
