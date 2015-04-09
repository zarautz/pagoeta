from django.db import models


class XeroxImage(models.Model):
    hash = models.CharField(max_length=40, unique=True)
    url = models.URLField(null=True, blank=True)

    class Meta(object):
        db_table = 'core_xerox'
