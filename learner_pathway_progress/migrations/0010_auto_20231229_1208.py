# Generated by Django 3.2.15 on 2023-12-29 05:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learner_pathway_progress', '0009_auto_20231229_1208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='author',
            name='date_of_death',
        ),
    ]