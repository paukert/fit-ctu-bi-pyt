from django.db import models


class QuestionType(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    class Meta:
        db_table = "question_type"
