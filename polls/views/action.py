import csv
import io
import textwrap

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from polls.models import Poll, PollState
from polls.configuration import *


@login_required(login_url='/polls/login/')
def export_results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if poll.owner_id != request.user.id:
        raise Http404('Poll not found')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="results.csv"'
    writer = csv.writer(response)

    row = ['Respondent']
    for question in poll.question_set.all():
        row.append(question.text)
        for option in question.option_set.all():
            row.append(option.text)
    writer.writerow(row)

    for answer in poll.answer_set.all():
        row = [answer.name]
        selected_options = answer.answerpart_set.values_list('option_id', flat=True)
        for question in poll.question_set.all():
            row.append(None)
            for option in question.option_set.all():
                if option.id in selected_options:
                    if question.question_type.name != 'Text answer':
                        row.append(1)
                    else:
                        row.append(answer.answerpart_set.filter(option_id=option.id).first().text)
                else:
                    row.append(None)
        writer.writerow(row)

    return response


@login_required(login_url='/polls/login/')
def generate_pdf(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if poll.owner_id != request.user.id:
        raise Http404('Poll not found')

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4, bottomup=0)
    text_object = pdf.beginText(PAGE_MARGINS, PAGE_MARGINS)

    text_object.setFont('Helvetica-Bold', 20)
    text_object.textLines(textwrap.fill(poll.name, 40))
    text_object.setFont('Helvetica', 12)
    for question_index, question in enumerate(poll.question_set.all()):
        text_object.textLine(f'Question #{question_index + 1}:')
        text_object.setFont('Helvetica-Oblique', 10)
        if question.question_type.name == 'Single choice':
            text_object.textLine('- choose single option')
        elif question.question_type.name == 'Multi choice':
            text_object.textLine('- choose 0-n options')
        else:
            text_object.textLine('- write answer')
        text_object.setFont('Helvetica', 12)
        text_object.moveCursor(0, 10)
        text_object.textLines(textwrap.fill(question.text, 60))

        options_count = question.option_set.count()
        for option_index, option in enumerate(question.option_set.all()):
            for line in f'{option_index + 1:>10}. {textwrap.fill(option.text, 55)}'.splitlines():
                text_object.textLine(line)
            if question.question_type.name == 'Text answer':
                text_object.moveCursor(0, 40)

            # check if content fits into the page, if not - create new page
            (x, y) = text_object.getCursor()
            if y + REQUIRED_SPACE_AFTER_OPTION > A4[1] or \
               (option_index + 1 == options_count and y + REQUIRED_SPACE_AFTER_QUESTION > A4[1]):
                pdf.drawText(text_object)
                pdf.showPage()
                text_object = pdf.beginText(PAGE_MARGINS, PAGE_MARGINS)

        text_object.moveCursor(0, 25)

    pdf.drawText(text_object)
    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='poll.pdf')


@login_required(login_url='/polls/login/')
def export_poll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if poll.owner_id != request.user.id:
        raise Http404('Poll not found')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="poll.csv"'
    writer = csv.writer(response)

    writer.writerow([poll.name])
    for question in poll.question_set.all():
        writer.writerow([question.text, question.order, question.question_type_id])
        for option in question.option_set.all():
            writer.writerow([option.text])
        writer.writerow(['---'])

    return response


# source: https://pythoncircle.com/post/30/how-to-upload-and-process-the-csv-file-in-django/
@login_required(login_url='/polls/login/')
def import_poll(request):
    if request.method != 'POST':
        return redirect('polls:admin')

    csv_file = request.FILES.get('file')
    if not csv_file:
        messages.error(request, 'No file selected to upload')
        return redirect('polls:admin')

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'Type of uploaded file is not CSV')
        return redirect('polls:admin')

    if csv_file.multiple_chunks():
        messages.error(request, f'Uploaded file is too big ({(csv_file.size / 1000000):.1f} MB)')
        return redirect('polls:admin')

    file_data = csv_file.read().decode("utf-8")
    lines = file_data.splitlines()

    if len(lines) == 0 or not lines[0]:
        messages.error(request, 'Error occurred while processing the file')
        return redirect('polls:admin')

    poll = Poll.objects.create(name=lines.pop(0), owner_id=request.user.id, state=PollState.objects.get(name='Draft'))

    try:
        while len(lines) > 0 and lines[0]:
            fields = lines.pop(0).split(',')
            question = poll.question_set.create(text=fields[0], order=fields[1], question_type_id=fields[2])

            while (line := lines.pop(0)) != '---':
                question.option_set.create(text=line)

    except Exception:
        poll.delete()
        messages.error(request, 'Error occurred while processing the file')
        return redirect('polls:admin')

    messages.success(request, 'Poll was imported successfully')
    return redirect('polls:admin')
