from django.conf import settings
from django.db import models

from polls.models import PollState


class Poll(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    state = models.ForeignKey(PollState, default=1, on_delete=models.RESTRICT)

    class Meta:
        db_table = "poll"

    def get_summary_results(self):
        results = []
        for question in self.question_set.all():
            if question.question_type.name != 'Text answer':
                results.append({'containChart': True, 'chart': question.get_chart()})
            else:
                results.append({'containChart': False, 'textAnswers': question.get_text_answers()})

        return {'name': self.name, 'results': results}
