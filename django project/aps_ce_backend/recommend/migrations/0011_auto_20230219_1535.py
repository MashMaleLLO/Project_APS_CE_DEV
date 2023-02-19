# Generated by Django 3.2.16 on 2023-02-19 15:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0010_auto_20230219_1357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student_grade',
            name='curriculum',
        ),
        migrations.AlterField(
            model_name='csv_file',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 19, 15, 35, 4, 431597, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='csv_file',
            name='upload_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 19, 15, 35, 4, 431548, tzinfo=utc)),
        ),
    ]
