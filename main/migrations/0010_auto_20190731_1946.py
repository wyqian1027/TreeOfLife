# Generated by Django 2.1.7 on 2019-07-31 19:46

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20190731_1926'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hierarchy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hierarchy_name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, default='scientific taxonomy hierarchy')),
            ],
            options={
                'verbose_name_plural': 'Hierarchies',
            },
        ),
        migrations.RemoveField(
            model_name='category',
            name='classification_type',
        ),
        migrations.AlterField(
            model_name='category',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 31, 19, 46, 15, 813760, tzinfo=utc), verbose_name='Date Created'),
        ),
        migrations.AddField(
            model_name='category',
            name='hierarchy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Hierarchy'),
        ),
    ]