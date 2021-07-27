from django.db import models

from polls.models import Question


class Option(models.Model):
    text = models.CharField(max_length=500)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        db_table = "option"
