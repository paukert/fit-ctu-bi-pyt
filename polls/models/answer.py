from django.db import models

from polls.models import Poll


class Answer(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    gdpr_agreement = models.BooleanField()
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    class Meta:
        db_table = "answer"
