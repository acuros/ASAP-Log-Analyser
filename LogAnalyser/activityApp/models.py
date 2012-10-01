from django.db import models

class Activity(models.Model):
    time = models.DateTimeField()
    name = models.CharField(max_length=50)
    return_code = models.CharField(max_length=30)
    reason = models.CharField(max_length=30)

    @classmethod
    def load_from_dictionary(cls, dictionary):
        activity = cls()
        activity.time=dictionary['time']
        activity.return_code = dictionary['Return code']
        activity.reason = dictionary['Reason']
        activity.save()

        key_value_class = ['GET', 'POST', 'COOKIES', 'SESSION', 'META', 'Response_variables']
        for class_name in key_value_class:
            eval(class_name).load_from_dictionary(activity, dictionary[class_name])
        

class KeyValueModel(models.Model):
    activity = models.ForeignKey(Activity)
    key = models.CharField(max_length=100)
    value = models.TextField()
    child_class = []

    @classmethod
    def load_from_dictionary(cls, activity, dictionary):
        model  = cls()
        model .activity = activity
        
        for key, value in dictionary.iteritems():
            model.key = key
            model.value = value
        model.save()

class GET(KeyValueModel):
    pass

class POST(KeyValueModel):
    pass

class COOKIES(KeyValueModel):
    pass

class SESSION(KeyValueModel):
    pass

class META(KeyValueModel):
    pass

class Response_variables(KeyValueModel):
    pass
