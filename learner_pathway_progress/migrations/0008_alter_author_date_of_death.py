# Generated by Django 3.2.15 on 2023-12-29 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learner_pathway_progress', '0007_auto_20231229_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='date_of_death',
            field=models.DateField(auto_now=True),
        ),
    ]
