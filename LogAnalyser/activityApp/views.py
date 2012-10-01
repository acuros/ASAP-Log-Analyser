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
