# Generated by Django 3.1.7 on 2021-05-07 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('date', models.DateTimeField()),
                ('gdpr_agreement', models.BooleanField()),
            ],
            options={
                'db_table': 'answer',
            },
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'poll',
            },
        ),
        migrations.CreateModel(
            name='PollState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'poll_state',
            },
        ),
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'question_type',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.poll')),
                ('question_type', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='polls.questiontype')),
            ],
            options={
                'db_table': 'question',
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='poll',
            name='state',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='polls.pollstate'),
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.question')),
            ],
            options={
                'db_table': 'option',
            },
        ),
        migrations.CreateModel(
            name='AnswerPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1000)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.answer')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.option')),
            ],
            options={
                'db_table': 'answer_part',
            },
        ),
        migrations.AddField(
            model_name='answer',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.poll'),
        ),
    ]