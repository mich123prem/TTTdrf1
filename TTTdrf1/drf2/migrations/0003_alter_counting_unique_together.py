# Generated by Django 4.0.3 on 2022-03-27 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drf2', '0002_remove_activityzone_starttime'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='counting',
            unique_together={('project', 'startTime')},
        ),
    ]
