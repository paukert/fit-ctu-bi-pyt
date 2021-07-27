from django.db import models
from plotly.offline import plot
import plotly.graph_objects as go

from polls.models import Poll, QuestionType


class Question(models.Model):
    text = models.CharField(max_length=500)
    order = models.IntegerField(null=True, blank=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    question_type = models.ForeignKey(QuestionType, on_delete=models.RESTRICT)

    class Meta:
        db_table = "question"
        ordering = ['order']

    def get_chart(self):
        answers = []
        option_names = []
        for option in self.option_set.all():
            answers.append(option.answerpart_set.count())
            option_names.append(option.text)

        if self.question_type.name == 'Single choice':
            fig = go.Figure(data=[go.Pie(labels=option_names, values=answers)])
            fig.update_layout(title=self.text)
        else:
            fig = go.Figure(data=[go.Bar(x=option_names, y=answers)])
            fig.update_layout(title=self.text, yaxis={'tickformat': ',d'})

        return plot(fig, output_type='div', include_plotlyjs=False)

    def get_text_answers(self):
        answers = []
        for option in self.option_set.all():
            option_answers = []
            for answer in option.answerpart_set.all():
                option_answers.append(answer.text)
            answers.append({'optionText': option.text, 'optionAnswers': option_answers})
        return {'text': self.text, 'answers': answers}
