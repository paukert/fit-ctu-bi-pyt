import csv
import io

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from polls.models import Poll, PollState, QuestionType


def create_poll_with_answers():
    user = User.objects.create_user(username='Lukas', password='SecretPassword')
    poll = Poll.objects.create(name='Sports', owner=user, state=PollState.objects.get(name='Active'))

    question_1 = poll.question_set.create(text='Sex', question_type=QuestionType.objects.get(name='Single choice'))
    option_1 = question_1.option_set.create(text='Male')
    option_2 = question_1.option_set.create(text='Female')

    answer_1 = poll.answer_set.create(name='Lukas', date=timezone.now(), gdpr_agreement=1)
    answer_1.answerpart_set.create(option=option_1)

    question_2 = poll.question_set.create(text='Other messages',
                                          question_type=QuestionType.objects.get(name='Text answer'))
    option_3 = question_2.option_set.create(text='Limit 300 words')
    answer_2 = poll.answer_set.create(name='Iva', date=timezone.now(), gdpr_agreement=1)
    answer_2.answerpart_set.create(option=option_2)
    answer_2.answerpart_set.create(text='Some text', option=option_3)

    return poll


class ActionExportResultsViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.poll = create_poll_with_answers()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('polls:export_results', args=(self.poll.id,)))
        self.assertEqual(response.status_code, 302)

    def test_csv_export(self):
        self.client.login(username='Lukas', password='SecretPassword')
        response = self.client.get(reverse('polls:export_results', args=(self.poll.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Disposition'), 'attachment; filename="results.csv"')

        content = response.content.decode('utf-8')
        cvs_reader = csv.reader(io.StringIO(content))
        body = list(cvs_reader)

        self.assertListEqual(body, [
            ['Respondent',  'Sex',  'Male', 'Female',   'Other messages',   'Limit 300 words'],
            ['Lukas',       '',     '1',    '',         '',                 ''],
            ['Iva',         '',     '',     '1',        '',                 'Some text']
        ])


class ActionGeneratePDFViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.poll = create_poll_with_answers()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('polls:generate_pdf', args=(self.poll.id,)))
        self.assertEqual(response.status_code, 302)

    def test_generating_pdf(self):
        self.client.login(username='Lukas', password='SecretPassword')
        response = self.client.get(reverse('polls:generate_pdf', args=(self.poll.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Disposition'), 'attachment; filename="poll.pdf"')


class ActionExportPollTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.poll = create_poll_with_answers()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('polls:export_poll', args=(self.poll.id,)))
        self.assertEqual(response.status_code, 302)

    def test_missing_poll(self):
        self.client.login(username='Lukas', password='SecretPassword')
        response = self.client.get(reverse('polls:export_poll', args=(5,)))
        self.assertEqual(response.status_code, 404)

    def test_exporting_poll(self):
        self.client.login(username='Lukas', password='SecretPassword')
        response = self.client.get(reverse('polls:export_poll', args=(self.poll.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.content.decode('utf-8').splitlines(), [
            'Sports',
            'Sex,,1',
            'Male',
            'Female',
            '---',
            'Other messages,,3',
            'Limit 300 words',
            '---'
        ])
