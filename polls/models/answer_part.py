from django.db import models

from polls.models import Answer, Option


class AnswerPart(models.Model):
    text = models.CharField(max_length=1000)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)

    class Meta:
        db_table = "answer_part"
