from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from polls.models import Poll, AnswerPart, Answer, Question


def index(request):
    error_message = ''

    if request.method == 'POST':
        poll_id = request.POST.get('poll_id')
        if poll_id:
            try:
                if Poll.objects.filter(pk=poll_id, state__name='Active').exists():
                    return redirect('polls:detail', poll_id=poll_id)
                else:
                    error_message = "Poll with entered ID doesn't exist."
            except ValueError:
                error_message = "Poll with entered ID doesn't exist."
        else:
            error_message = 'Poll ID has to be entered.'

    return render(request, 'polls/index.html', {'error_message': error_message})


def detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id, state__name="Active")
    return render(request, 'polls/detail.html', {'poll': poll})


def vote(request, poll_id):
    # check if someone did not send other request than POST to polls/ID/vote/
    # if it is POST request, identity is verified by CSRF token
    if request.method != 'POST':
        return redirect('polls:index')

    get_object_or_404(Poll, pk=poll_id, state__name="Active")

    gdpr = 1 if 'gdpr' in request.POST else 0
    name = request.POST.get('name') if gdpr == 1 and request.POST.get('name') else 'Anonymous user'
    answer = Answer.objects.create(name=name, date=timezone.now(), gdpr_agreement=gdpr, poll_id=poll_id)

    for key, value in request.POST.items():
        if key == 'csrfmiddlewaretoken' or key == 'name' or key == 'gdpr':
            continue

        if key.startswith('question-'):
            key = value

        try:
            question = Question.objects.filter(option__id=key, poll_id=poll_id).first()
            if question.question_type.name != 'Text answer':
                AnswerPart.objects.create(answer_id=answer.id, option_id=key)
            elif value:
                AnswerPart.objects.create(answer_id=answer.id, option_id=key, text=value)
        except ValueError:
            pass

    return redirect('polls:thankyou')


def thankyou(request):
    return render(request, 'polls/thankyou.html')
