# Generated by Django 4.0.3 on 2022-04-06 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drf2', '0004_project_activities'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zone',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zone', to='drf2.project'),
        ),
    ]