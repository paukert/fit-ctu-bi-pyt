from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from polls.models import Poll, PollState, QuestionType


def create_user():
    return User.objects.create_user(username='Lukas', password='SecretPassword')


class PollIndexViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = create_user()

    def test_response(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)

    def test_missing_poll(self):
        response = self.client.post(reverse('polls:index'), {'poll_id': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error_message'], "Poll with entered ID doesn't exist.")

    def test_not_filled_poll(self):
        response = self.client.post(reverse('polls:index'), {'poll_id': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error_message'], 'Poll ID has to be entered.')

    def test_draft_poll(self):
        poll = Poll.objects.create(name='Test poll', owner=self.owner, state=PollState.objects.get(name='Draft'))
        response = self.client.post(reverse('polls:index'), {'poll_id': poll.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error_message'], "Poll with entered ID doesn't exist.")

    def test_active_poll(self):
        poll = Poll.objects.create(name='Test poll', owner=self.owner, state=PollState.objects.get(name='Active'))
        response = self.client.post(reverse('polls:index'), {'poll_id': poll.id})
        self.assertEqual(response.status_code, 302)

    def test_closed_poll(self):
        poll = Poll.objects.create(name='Test poll', owner=self.owner, state=PollState.objects.get(name='Closed'))
        response = self.client.post(reverse('polls:index'), {'poll_id': poll.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error_message'], "Poll with entered ID doesn't exist.")


class PollDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = create_user()

    def test_draft_poll(self):
        poll = Poll.objects.create(name='Test poll', owner=self.owner, state=PollState.objects.get(name='Draft'))
        response = self.client.get(reverse('polls:detail', args=(poll.id,)))
        self.assertEqual(response.status_code, 404)

    def test_active_poll(self):
        poll = Poll.objects.create(name='Test poll', owner=self.owner, state=PollState.objects.get(name='Active'))
        response = self.client.get(reverse('polls:detail', args=(poll.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['poll'], poll)

    def test_closed_poll(self):
        poll = Poll.objects.create(name='Test poll', owner=self.owner, state=PollState.objects.get(name='Closed'))
        response = self.client.get(reverse('polls:detail', args=(poll.id,)))
        self.assertEqual(response.status_code, 404)

    def test_missing_poll(self):
        response = self.client.get(reverse('polls:detail', args=(5,)))
        self.assertEqual(response.status_code, 404)


class PollVoteViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = create_user()
        cls.poll = Poll.objects.create(name='Sports', owner=cls.owner, state=PollState.objects.get(name='Active'))

    def test_redirect_if_not_post(self):
        response = self.client.get(reverse('polls:vote', args=(self.poll.id,)))
        self.assertEqual(response.status_code, 302)

    def test_draft_poll(self):
        poll = Poll.objects.create(name='Test poll', owner=self.owner, state=PollState.objects.get(name='Draft'))
        response = self.client.post(reverse('polls:vote', args=(poll.id,)))
        self.assertEqual(response.status_code, 404)

    def test_closed_poll(self):
        poll = Poll.objects.create(name='Test poll', owner=self.owner, state=PollState.objects.get(name='Closed'))
        response = self.client.post(reverse('polls:vote', args=(poll.id,)))
        self.assertEqual(response.status_code, 404)

    def test_gdpr_poll(self):
        response = self.client.post(reverse('polls:vote', args=(self.poll.id,)), {'name': 'Lukas'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual('Anonymous user', self.poll.answer_set.first().name)

    def test_saving_single_option_question(self):
        question = self.poll.question_set.create(text='Sex',
                                                 question_type=QuestionType.objects.get(name='Single choice'))
        option = question.option_set.create(text='Male')
        question.option_set.create(text='Female')

        response = self.client.post(reverse('polls:vote', args=(self.poll.id,)), {
            'name': 'Lukas',
            'gdpr': 'on',
            'question-' + str(question.id): option.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual('Lukas', self.poll.answer_set.first().name)
        self.assertEqual(1, option.answerpart_set.count())
        self.assertEqual('', option.answerpart_set.first().text)

    def test_saving_multi_option_question(self):
        question = self.poll.question_set.create(text='Select your favourite sports',
                                                 question_type=QuestionType.objects.get(name='Multi choice'))
        option_1 = question.option_set.create(text='Running')
        option_2 = question.option_set.create(text='Swimming')

        response = self.client.post(reverse('polls:vote', args=(self.poll.id,)), {
            'name': 'Lukas',
            option_1.id: 'on',
            option_2.id: 'on'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual('Anonymous user', self.poll.answer_set.first().name)
        self.assertEqual(1, option_1.answerpart_set.count())
        self.assertEqual(1, option_2.answerpart_set.count())
        self.assertEqual('', option_1.answerpart_set.first().text)
        self.assertEqual('', option_2.answerpart_set.first().text)

    def test_saving_text_answers(self):
        question = self.poll.question_set.create(text='Other messages',
                                                 question_type=QuestionType.objects.get(name='Text answer'))
        option = question.option_set.create(text='Limit 300 words')

        response = self.client.post(reverse('polls:vote', args=(self.poll.id,)), {option.id: 'Hello world'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(1, option.answerpart_set.count())
        self.assertEqual('Hello world', option.answerpart_set.first().text)


class PollThankYouViewTests(TestCase):
    def test_response(self):
        response = self.client.get(reverse('polls:thankyou'))
        self.assertEqual(response.status_code, 200)
