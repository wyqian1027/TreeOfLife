# Generated by Django 2.1.7 on 2019-08-02 17:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20190801_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 2, 17, 30, 55, 564872, tzinfo=utc), verbose_name='Date Created'),
        ),
    ]
