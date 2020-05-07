# Generated by Django 3.0.5 on 2020-05-07 19:36

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectp1',
            name='project_name',
        ),
        migrations.RemoveField(
            model_name='projectp1',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='projectp1',
            name='tender',
        ),
        migrations.AddField(
            model_name='projectp1',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Projects'),
        ),
        migrations.AlterField(
            model_name='projectp1',
            name='ahts',
            field=models.DateField(default=django.utils.timezone.now, null=True, verbose_name='Agreement Handover to Supervisor Date'),
        ),
        migrations.AlterField(
            model_name='projectp1',
            name='asd',
            field=models.DateField(default=django.utils.timezone.now, null=True, verbose_name='Agreement Submission Date'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='project_start_date',
            field=models.DateField(default=datetime.datetime(2020, 5, 7, 19, 36, 24, 356022, tzinfo=utc), null=True, verbose_name='Project Start Date'),
        ),
        migrations.CreateModel(
            name='ProjectP2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover_letter', models.FileField(upload_to='', verbose_name='Covering Letter Copy')),
                ('invoice_copy', models.FileField(upload_to='', verbose_name='Invoice Copy')),
                ('atten_sheet', models.FileField(upload_to='', verbose_name='Attendance Sheet Copy')),
                ('salary_sheet', models.FileField(upload_to='', verbose_name='Salary Sheet Copy')),
                ('bank_statement', models.FileField(upload_to='', verbose_name='Bank Statement Copy')),
                ('epf_chalan', models.FileField(upload_to='', verbose_name='EPF Chalan (Upload)')),
                ('epf_ecr', models.FileField(upload_to='', verbose_name='EPF ECR (Upload)')),
                ('esic_chalan', models.FileField(upload_to='', verbose_name='ESIC Chalan (Upload)')),
                ('esic_ecr', models.FileField(upload_to='', verbose_name='ESIC ECR (Upload)')),
                ('labor_passbook', models.FileField(upload_to='', verbose_name='Labore Passbook / BS (Upload)')),
                ('doc_handover_date', models.DateField(default=datetime.datetime(2020, 5, 7, 19, 36, 24, 358020, tzinfo=utc), verbose_name='All Document Handover Date')),
                ('doc_handover_to', models.CharField(max_length=50, null=True, verbose_name='All Document Handover to (Person Name)')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Projects')),
            ],
            options={
                'verbose_name': 'Project Phase - 2',
                'verbose_name_plural': 'Project Phase - 2',
            },
        ),
        migrations.CreateModel(
            name='ProjectFollowup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Current Date & Time')),
                ('followup_by', models.CharField(max_length=200, null=True)),
                ('foolowup_to', models.CharField(max_length=200, null=True)),
                ('foolowup_remarks', models.CharField(max_length=500, null=True)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Projects')),
            ],
            options={
                'verbose_name': 'Project Followup',
                'verbose_name_plural': 'Project Followup',
            },
        ),
    ]