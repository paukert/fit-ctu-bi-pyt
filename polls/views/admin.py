from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from polls.configuration import *
from polls.models import Poll, Answer, Option, Question, QuestionType


@login_required(login_url='/polls/login/')
def admin(request):
    created_polls = Poll.objects.filter(owner_id=request.user.id)
    if request.method == 'POST':
        poll_name = request.POST.get('newPollName')
        if poll_name and len(poll_name) >= POLL_NAME_MIN_LENGTH:
            Poll.objects.create(name=poll_name, owner_id=request.user.id)

    return render(request, 'polls/admin.html', {'polls': created_polls, 'pollNameMinLength': POLL_NAME_MIN_LENGTH})


@login_required(login_url='/polls/login/')
def edit(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if poll.owner_id != request.user.id:
        raise Http404('Poll not found')

    question_types = QuestionType.objects.all()
    error_message = ''

    if request.method == 'POST' and poll.state.name == 'Draft':
        poll_name = request.POST.get('pollName')
        if poll_name and len(poll_name) >= POLL_NAME_MIN_LENGTH:
            poll.name = poll_name
            poll.save()

        for question in poll.question_set.all():
            qText = request.POST.get('qText' + str(question.id))
            order = request.POST.get('qOrder' + str(question.id))
            qOrder = order if order else None  # check if order is not an empty string
            try:
                qType = QuestionType.objects.get(id=request.POST.get('qType' + str(question.id)))
            except (QuestionType.DoesNotExist, ValueError):
                qType = None

            # should be always true if user did not send POST request on his own
            if qText and len(qText) >= QUESTION_TEXT_MIN_LENGTH and qType:
                question.text = qText
                question.order = qOrder
                question.question_type = qType
                question.save()

            for option in question.option_set.all():
                oText = request.POST.get('oText' + str(option.id))
                if oText and len(oText) >= OPTION_TEXT_MIN_LENGTH:  # also should be always true
                    option.text = oText
                    option.save()

        # add new question
        if request.POST.get('addNewQuestion'):
            qText = request.POST.get('qTextNew')
            order = request.POST.get('qOrderNew')
            qOrder = order if order else None
            try:
                qType = QuestionType.objects.get(id=request.POST.get('qTypeNew'))
            except (QuestionType.DoesNotExist, ValueError):
                qType = None

            if qText and len(qText) >= QUESTION_TEXT_MIN_LENGTH and qType:
                poll.question_set.create(text=qText, order=qOrder, question_type=qType)

        # add new option
        elif request.POST.get('addNewOption'):
            for k, v in request.POST.items():
                if v and k.startswith('oTextNew'):
                    try:
                        question = poll.question_set.get(id=k[8:])
                    except (Question.DoesNotExist, ValueError):
                        question = None
                    if len(v) >= OPTION_TEXT_MIN_LENGTH and question:
                        question.option_set.create(text=v)

        # delete option
        elif request.POST.get('deleteOption'):
            try:
                option = Option.objects.get(id=request.POST.get('deleteOption'))
            except (Question.DoesNotExist, ValueError):
                return redirect('polls:admin')
            if poll.question_set.filter(option__exact=option).exists():
                option.delete()

        # delete question
        elif request.POST.get('deleteQuestion'):
            try:
                poll.question_set.get(id=request.POST.get('deleteQuestion')).delete()
            except (Question.DoesNotExist, ValueError):
                return redirect('polls:admin')

        elif request.POST.get('deletePoll'):
            poll.delete()
            return redirect('polls:admin')

        elif request.POST.get('changeState'):
            poll.state_id = 2
            poll.save()

    elif request.method == 'POST' and request.POST.get('changeState') and poll.state.name == 'Active':
        poll.state_id = 3
        poll.save()

    elif request.method == 'POST':
        error_message = "Cannot edit the poll, its state is not 'Draft' anymore!"

    return render(request, 'polls/edit.html', {'poll': poll,
                                               'questionTypes': question_types,
                                               'optionTextMinLength': OPTION_TEXT_MIN_LENGTH,
                                               'pollNameMinLength': POLL_NAME_MIN_LENGTH,
                                               'questionTextMinLength': QUESTION_TEXT_MIN_LENGTH,
                                               'error': error_message})


@login_required(login_url='/polls/login/')
def summary_results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if poll.owner_id != request.user.id:
        raise Http404('Poll not found')
    if not poll.answer_set.exists():
        return render(request, 'polls/summary-results.html', {'name': poll.name, 'error': 'No results yet'})

    return render(request, 'polls/summary-results.html', poll.get_summary_results())


@login_required(login_url='/polls/login/')
def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if poll.owner_id != request.user.id:
        raise Http404('Poll not found')
    if not poll.answer_set.exists():
        return render(request, 'polls/results.html', {'name': poll.name, 'error': 'No results yet'})

    return render(request, 'polls/results.html', {'id': poll_id, 'name': poll.name, 'answers': poll.answer_set.all()})


@login_required(login_url='/polls/login/')
def single_result(request, poll_id, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    poll = get_object_or_404(Poll, pk=poll_id)
    if poll.owner_id != request.user.id or answer.poll_id != poll.id:
        raise Http404('Poll not found')

    questions = []
    for question in poll.question_set.all():
        questions.append({'text': question.text,
                          'type': question.question_type.name,
                          'answers': answer.answerpart_set.filter(option__in=question.option_set.all())})

    return render(request, 'polls/single-result.html', {'name': poll.name,
                                                        'date': answer.date,
                                                        'respondent': answer.name,
                                                        'questions': questions})
