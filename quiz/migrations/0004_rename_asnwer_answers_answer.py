# Generated by Django 4.1.5 on 2023-01-26 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_remove_answers_points_answers_is_correct'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answers',
            old_name='asnwer',
            new_name='answer',
        ),
    ]
