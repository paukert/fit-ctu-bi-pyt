from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from polls.models import Poll, PollState, Question, QuestionType


def create_question(text, poll, question_type, order=None):
    return Question.objects.create(text=text, poll=poll, question_type=question_type, order=order)


class QuestionModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(username='Lukas', password='SecretPassword')
        cls.poll = Poll.objects.create(name='Test poll', owner=cls.owner, state=PollState.objects.get(name='Draft'))

    def test_get_chart_single_choice(self):
        question = create_question('Sex', self.poll, QuestionType.objects.get(name='Single choice'))
        question.option_set.create(text='Male')
        question.option_set.create(text='Female')

        chart = question.get_chart()
        self.assertIn('Sex', chart)
        self.assertIn('Male', chart)
        self.assertIn('Female', chart)

    def test_get_chart_multi_choice(self):
        question = create_question('Select favourite sports', self.poll, QuestionType.objects.get(name='Multi choice'))
        question.option_set.create(text='Tennis')
        question.option_set.create(text='Running')
        question.option_set.create(text='Swimming')

        chart = question.get_chart()
        self.assertIn('Select favourite sports', chart)
        self.assertIn('Tennis', chart)
        self.assertIn('Running', chart)
        self.assertIn('Swimming', chart)

    def test_get_text_answers(self):
        question = create_question('Name sportsman who:', self.poll, QuestionType.objects.get(name='Text answer'))
        option_1 = question.option_set.create(text='plays tennis')
        option_2 = question.option_set.create(text='is football player')
        answer_1 = self.poll.answer_set.create(name='Lukas', date=timezone.now(), gdpr_agreement=1)
        answer_2 = self.poll.answer_set.create(name='Tomas', date=timezone.now(), gdpr_agreement=1)
        option_1.answerpart_set.create(text='Radek Stepanek', answer=answer_1)
        option_1.answerpart_set.create(text='Tomas Berdych', answer=answer_2)
        option_2.answerpart_set.create(text='Lionel Messi', answer=answer_1)

        self.assertDictEqual(question.get_text_answers(), {
            'text': 'Name sportsman who:',
            'answers': [
                {
                    'optionText': 'plays tennis',
                    'optionAnswers': ['Radek Stepanek', 'Tomas Berdych']
                },
                {
                    'optionText': 'is football player',
                    'optionAnswers': ['Lionel Messi']
                }
            ]
        })

    def test_get_text_answers_empty(self):
        question = create_question('Name sportsman who:', self.poll, QuestionType.objects.get(name='Text answer'))
        question.option_set.create(text='plays tennis')
        question.option_set.create(text='is football player')

        self.assertDictEqual(question.get_text_answers(), {
            'text': 'Name sportsman who:',
            'answers': [
                {
                    'optionText': 'plays tennis',
                    'optionAnswers': []
                },
                {
                    'optionText': 'is football player',
                    'optionAnswers': []
                }
            ]
        })
