# Generated by Django 3.2.16 on 2023-02-11 16:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0006_student_start_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='CSV_File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('upload_date', models.DateTimeField(default=datetime.datetime(2023, 2, 11, 16, 1, 26, 378869, tzinfo=utc))),
                ('update_date', models.DateTimeField(default=datetime.datetime(2023, 2, 11, 16, 1, 26, 378937, tzinfo=utc))),
                ('del_flag', models.CharField(max_length=10)),
                ('type_data', models.CharField(max_length=100)),
                ('file', picklefield.fields.PickledObjectField(editable=False)),
            ],
        ),
    ]