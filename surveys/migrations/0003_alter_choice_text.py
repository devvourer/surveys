# Generated by Django 3.2.7 on 2021-09-11 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0002_alter_survey_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='text',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
