# Generated by Django 5.0.7 on 2024-09-04 01:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_estimatedwaittime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='estimatedwaittime',
            old_name='waitEstimate',
            new_name='waitingTime',
        ),
    ]
