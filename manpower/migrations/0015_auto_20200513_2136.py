# Generated by Django 3.0.5 on 2020-05-13 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manpower', '0014_auto_20200513_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='overtime',
            field=models.CharField(choices=[(0, ''), ('A', 'A'), ('B', 'B'), ('C', 'C')], default='', max_length=12, null=True, verbose_name='Overtime'),
        ),
    ]
