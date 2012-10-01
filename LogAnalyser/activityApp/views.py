import datetime
from acuros_sap import ASAP
from activityApp.models import *

class CountHourlyView(ASAP):
    def process_get_request(self):
        date_start = datetime.datetime.strptime(self.get_get_parameter('date'), '%Y-%m-%d')
        date_end = date_start + datetime.timedelta(days=1)
        
        activities = Activity.objects.filter(time__gte = date_start, time__lt = date_end)
        hour_count = dict()
        [hour_count.setdefault(x, 0) for x in xrange(24)]
        for activity in activities:
            hour_count[activity.time.hour] += 1

        return dict(hour_count=hour_count)

class CountUniqueUserView(ASAP):
    def process_get_request(self):
        trace_hash_datas = SESSION.objects.get_query_set().filter(key='trace_hash')
        unique_user_count = dict()
        for idx in range(0,len(trace_hash_datas)):
            if unique_user_count.has_key(trace_hash_datas[idx].value):
                unique_user_count[trace_hash_datas[idx].value]+=1
            else:
                unique_user_count[trace_hash_datas[idx].value]=0

        return dict(unique_user_count=unique_user_count)
                
