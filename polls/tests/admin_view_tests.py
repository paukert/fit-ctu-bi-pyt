from django.contrib import auth
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from polls.models import Option, Poll, PollState, Question, QuestionType


def create_poll():
    user = User.objects.create_user(username='Lukas', password='SecretPassword')
    poll = Poll.objects.create(name='Sports', owner=user, state=PollState.objects.get(name='Closed'))
    question_1 = poll.question_set.create(text='Sex', question_type=QuestionType.objects.get(name='Single choice'))
    question_1.option_set.create(text='Male')
    question_1.option_set.create(text='Female')

    return poll


class AdminViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.poll = create_poll()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('polls:admin'))
        self.assertEqual(response.status_code, 302)

    def test_response(self):
        self.client.login(username='Lukas', password='SecretPassword')
        response = self.client.get(reverse('polls:admin'))
        self.assertEqual(response.status_code, 200)

    def test_adding_poll(self):
        self.client.login(username='Lukas', password='SecretPassword')
        poll_count = Poll.objects.filter(owner=auth.get_user(self.client)).count()
        response = self.client.post(reverse('polls:admin'), {'newPollName': 'New poll!'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Poll.objects.filter(owner=auth.get_user(self.client)).count(), poll_count + 1)


class AdminEditViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.poll = create_poll()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('polls:edit', args=(self.poll.id,)))
        self.assertEqual(response.status_code, 302)

    def test_missing_poll(self):
        self.client.login(username='Lukas', password='SecretPassword')
        response = self.client.get(reverse('polls:edit', args=(5,)))
        self.assertEqual(response.status_code, 404)

    def test_editing_active_poll(self):
        self.client.login(username='Lukas', password='SecretPassword')
        self.poll.state = PollState.objects.get(name='Active')
        self.poll.save()
        response = self.client.post(reverse('polls:edit', args=(self.poll.id,)), {'pollName': 'New poll name'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], "Cannot edit the poll, its state is not 'Draft' anymore!")

    def test_editing_closed_poll(self):
        self.client.login(username='Lukas', password='SecretPassword')
        response = self.client.post(reverse('polls:edit', args=(self.poll.id,)), {'pollName': 'New poll name'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], "Cannot edit the poll, its state is not 'Draft' anymore!")

    def test_change_state(self):
        self.client.login(username='Lukas', password='SecretPassword')
        self.poll.state = PollState.objects.get(name='Active')
        self.poll.save()
        response = self.client.post(reverse('polls:edit', args=(self.poll.id,)), {'changeState': 'changeState'})
        self.assertEqual(response.status_code, 200)
        self.poll = Poll.objects.get(id=self.poll.id)  # object has to be reloaded
        self.assertEqual(self.poll.state, PollState.objects.get(name='Closed'))

    def test_editing_poll(self):
        self.client.login(username='Lukas', password='SecretPassword')
        self.poll.state = PollState.objects.get(name='Draft')
        self.poll.save()
        question = self.poll.question_set.first()
        option = question.option_set.first()
        response = self.client.post(reverse('polls:edit', args=(self.poll.id,)), {
            'pollName': 'New poll name',
            'qText' + str(question.id): 'Gender',
            'qOrder' + str(question.id): 1,
            'qType' + str(question.id): 2,
            'oText' + str(option.id): 'Male male'
        })
        self.poll = Poll.objects.get(id=self.poll.id)  # object has to be reloaded
        question = self.poll.question_set.first()  # object has to be reloaded
        option = question.option_set.first()  # object has to be reloaded

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.poll.name, 'New poll name')
        self.assertEqual(question.text, 'Gender')
        self.assertEqual(question.order, 1)
        self.assertEqual(question.question_type, QuestionType.objects.get(id=2))
        self.assertEqual(option.text, 'Male male')

    def test_adding_question(self):
        self.client.login(username='Lukas', password='SecretPassword')
        self.poll.state = PollState.objects.get(name='Draft')
        self.poll.save()
        response = self.client.post(reverse('polls:edit', args=(self.poll.id,)), {
            'addNewQuestion': 'addNewQuestion',
            'qTextNew': 'New question',
            'qOrderNew': 2,
            'qTypeNew': 1,
        })
        question = Question.objects.filter(text='New question').first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(question.order, 2)
        self.assertEqual(question.question_type, QuestionType.objects.get(id=1))

    def test_adding_option(self):
        self.client.login(username='Lukas', password='SecretPassword')
        self.poll.state = PollState.objects.get(name='Draft')
        self.poll.save()
        question = self.poll.question_set.first()
        response = self.client.post(reverse('polls:edit', args=(self.poll.id,)), {
            'addNewOption': 'addNewOption',
            'oTextNew' + str(question.id): 'New option',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(question.option_set.filter(text='New option').exists())

    def test_deleting_option(self):
        self.client.login(username='Lukas', password='SecretPassword')
        self.poll.state = PollState.objects.get(name='Draft')
        self.poll.save()
        option = Option.objects.get(text='Male')
        response = self.client.post(reverse('polls:edit', args=(self.poll.id,)), {'deleteOption': option.id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Option.objects.filter(text='Male').exists())

    def test_deleting_question(self):
        self.client.login(username='Lukas', password='SecretPassword')
        self.poll.state = PollState.objects.get(name='Draft')
        self.poll.save()
        question = self.poll.question_set.first()
        response = self.client.post(reverse('polls:edit', args=(self.poll.id,)), {'deleteQuestion': question.id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.poll.question_set.exists())

    def test_deleting_poll(self):
        self.client.login(username='Lukas', password='SecretPassword')
        self.poll.state = PollState.objects.get(name='Draft')
        self.poll.save()
        response = self.client.post(reverse('polls:edit', args=(self.poll.id,)), {'deletePoll': 'deletePoll'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Poll.objects.count(), 0)


class AdminSummaryResultsViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.poll = create_poll()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('polls:summary_results', args=(self.poll.id,)))
        self.assertEqual(response.status_code, 302)

    def test_missing_poll(self):
        self.client.login(username='Lukas', password='SecretPassword')
        response = self.client.get(reverse('polls:summary_results', args=(5,)))
        self.assertEqual(response.status_code, 404)

    def test_no_answers(self):
        self.client.login(username='Lukas', password='SecretPassword')
        response = self.client.get(reverse('polls:summary_results', args=(self.poll.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], 'No results yet')

    def test_with_answers(self):
        self.client.login(username='Lukas', password='SecretPassword')
        answer = self.poll.answer_set.create(name='Lukas', date=timezone.now(), gdpr_agreement=1)
        answer.answerpart_set.create(option=Option.objects.get(text='Male'))
        response = self.client.get(reverse('polls:summary_results', args=(self.poll.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('error', response.context)


class AdminResultsViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.poll = create_poll()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('polls:results', args=(self.poll.id,)))
        self.assertEqual(response.status_code, 302)

    def test_missing_poll(self):
        self.client.login(username='Lukas', password='SecretPassword')
        response = self.client.get(reverse('polls:results', args=(5,)))
        self.assertEqual(response.status_code, 404)

    def test_no_answers(self):
        self.client.login(username='Lukas', password='SecretPassword')
        response = self.client.get(reverse('polls:results', args=(self.poll.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], 'No results yet')

    def test_with_answers(self):
        self.client.login(username='Lukas', password='SecretPassword')
        answer = self.poll.answer_set.create(name='Lukas', date=timezone.now(), gdpr_agreement=1)
        answer.answerpart_set.create(option=Option.objects.get(text='Male'))
        response = self.client.get(reverse('polls:results', args=(self.poll.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('error', response.context)


class AdminSingleResultViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.poll = create_poll()
        cls.answer = cls.poll.answer_set.create(name='Lukas', date=timezone.now(), gdpr_agreement=1)
        cls.answer.answerpart_set.create(option=Option.objects.get(text='Male'))

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('polls:single_result', args=(self.poll.id, self.answer.id)))
        self.assertEqual(response.status_code, 302)

    def test_missing_poll(self):
        self.client.login(username='Lukas', password='SecretPassword')
        response = self.client.get(reverse('polls:single_result', args=(5, self.answer.id)))
        self.assertEqual(response.status_code, 404)

    def test_missing_answer(self):
        self.client.login(username='Lukas', password='SecretPassword')
        response = self.client.get(reverse('polls:single_result', args=(self.poll.id, 5)))
        self.assertEqual(response.status_code, 404)

    def test_answers(self):
        self.client.login(username='Lukas', password='SecretPassword')
        response = self.client.get(reverse('polls:single_result', args=(self.poll.id, self.answer.id)))
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context['questions'], [])
