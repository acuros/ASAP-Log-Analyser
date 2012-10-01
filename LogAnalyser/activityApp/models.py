from django.db import models

class Activity(models.Model):
    time = models.DateField()
    return_code = models.CharField(max_length=30)
    reason = models.CharField(max_length=30)
    response_variables = models.TextField()

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
