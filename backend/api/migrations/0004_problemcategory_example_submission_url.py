# Generated by Django 5.0.4 on 2024-06-19 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_submission_is_downloadable_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='problemcategory',
            name='example_submission_url',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]