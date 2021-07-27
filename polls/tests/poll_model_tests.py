from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from polls.models import Poll, PollState, QuestionType


class PollModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(username='Lukas', password='SecretPassword')
        cls.poll = Poll.objects.create(name='Test poll', owner=cls.owner, state=PollState.objects.get(name='Draft'))

    def test_get_summary_results(self):
        question = self.poll.question_set.create(text='Name sportsman who:',
                                                 question_type=QuestionType.objects.get(name='Text answer'))
        option = question.option_set.create(text='plays tennis')
        question.option_set.create(text='is football player')
        answer = self.poll.answer_set.create(name='Lukas', date=timezone.now(), gdpr_agreement=1)
        answer.answerpart_set.create(text='Radek Stepanek', option=option)

        self.poll.question_set.create(text='What are you not satisfied with?',
                                      question_type=QuestionType.objects.get(name='Text answer'))

        self.assertDictEqual(self.poll.get_summary_results(), {
            'name': 'Test poll',
            'results': [
                {
                    'containChart': False,
                    'textAnswers': {
                        'text': 'Name sportsman who:',
                        'answers': [
                            {
                                'optionText': 'plays tennis',
                                'optionAnswers': ['Radek Stepanek']
                            },
                            {
                                'optionText': 'is football player',
                                'optionAnswers': []
                            }
                        ]
                    }
                },
                {
                    'containChart': False,
                    'textAnswers': {
                        'text': 'What are you not satisfied with?',
                        'answers': []
                    }
                }
            ]
        })

    def test_get_summary_results_empty(self):
        self.assertDictEqual(self.poll.get_summary_results(), {
            'name': 'Test poll',
            'results': []
        })
