# Generated by Django 3.0.5 on 2020-05-08 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_auto_20200508_1909'),
        ('manpower', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labour',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Projects'),
        ),
        migrations.DeleteModel(
            name='Attendance',
        ),
    ]