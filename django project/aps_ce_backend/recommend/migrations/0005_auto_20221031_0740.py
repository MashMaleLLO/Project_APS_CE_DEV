# Generated by Django 3.2.16 on 2022-10-31 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0004_surprisemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='career',
            field=models.CharField(default='Zero', max_length=100),
        ),
        migrations.AddField(
            model_name='student',
            name='status',
            field=models.CharField(default='ungraduate', max_length=100),
        ),
    ]
