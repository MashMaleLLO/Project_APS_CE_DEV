# Generated by Django 3.2.16 on 2023-02-22 16:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0012_auto_20230222_1529'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='surprisemodel',
            name='args',
        ),
        migrations.AddField(
            model_name='surprisemodel',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 22, 16, 40, 0, 571738, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='surprisemodel',
            name='del_flag',
            field=models.CharField(default=0, max_length=10),
        ),
        migrations.AddField(
            model_name='surprisemodel',
            name='name',
            field=models.CharField(default='rec_model', max_length=300),
        ),
        migrations.AddField(
            model_name='surprisemodel',
            name='rec_model',
            field=picklefield.fields.PickledObjectField(default='Zero', editable=False),
        ),
        migrations.AddField(
            model_name='surprisemodel',
            name='type_pred',
            field=models.CharField(default='Zero', max_length=100),
        ),
        migrations.AddField(
            model_name='surprisemodel',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 22, 16, 40, 0, 571777, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='csv_file',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 22, 16, 40, 0, 572420, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='csv_file',
            name='upload_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 22, 16, 40, 0, 572392, tzinfo=utc)),
        ),
    ]
