# Generated by Django 3.2.16 on 2022-11-14 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0005_auto_20221031_0740'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='start_year',
            field=models.CharField(default='Zero', max_length=100),
        ),
    ]