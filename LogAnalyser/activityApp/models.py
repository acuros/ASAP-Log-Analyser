from django.db import models

class Activity(models.Model):
    time = models.DateField()
    name = models.CharField(max_length=50)
    return_code = models.CharField(max_length=30)
    reason = models.CharField(max_length=30)

class KeyValueModel(models.Model):
    activity = models.ForeignKey(Activity)
    key = models.CharField(max_length=100)
    value = models.TextField()

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

class ResponseVariables(KeyValueModel):
    pass
