from django.db import models

from core.models import User


class Error(models.Model):
    content_id = models.IntegerField()
    line_id = models.IntegerField()
    order = models.IntegerField()
    correct = models.CharField(max_length=100)
    wrong = models.CharField(max_length=100)
    request_id = models.CharField(max_length=64)
    datetime = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='%(class)s_wordgaps_errors')

    class Meta:
        get_latest_by = 'datetime'
