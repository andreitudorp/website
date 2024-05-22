# Generated by Django 5.0.4 on 2024-05-22 10:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_specifiedproblem_evualuation_settings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='problem',
        ),
        migrations.AddField(
            model_name='submission',
            name='problem_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.specifiedproblem'),
        ),
    ]