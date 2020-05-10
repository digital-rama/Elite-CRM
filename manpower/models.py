from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from project.models import *


class SuperVisors(models.Model):
    username = models.CharField(
        'Username', max_length=50, blank=False, unique=True)
    password = models.CharField('Password', max_length=50, blank=False)
    re_password = models.CharField(
        'Confirm Password', max_length=50, blank=False)
    name = models.CharField('Supervisor Name', max_length=250, blank=False)
    dateofbirth = models.DateField('Date of Birth', default=timezone.now)
    image = models.FileField('Profile Picture', blank=False, null=False)
    mobile_number = models.CharField('Mobile Number', max_length=15)
    alter_number = models.CharField('Alternate Number', max_length=15)
    email = models.EmailField(
        'Email Address', null=True, blank=True, unique=True)
    address = models.CharField('Supervisor Address', max_length=500)
    resume = models.FileField(
        'Upload Supervisor Resume', blank=False, null=False)
    aadhar_number = models.CharField('Aadhar Number', max_length=20)
    aadhar_photo = models.FileField(
        'Aadhar Card Scan Copy', blank=False, null=False)
    pan_number = models.CharField('PAN Card Number', max_length=20)
    pan_photo = models.FileField('PAN Card Scan Copy', blank=False, null=False)
    highest_qual = models.CharField('Highest Qualifications', max_length=200)
    highest_qual_photo = models.FileField(
        'Proof of Highest Qualification', blank=False)
    ten_certi = models.FileField('10th Certificate', blank=False)
    twelve_certi = models.FileField('12th Certificate', blank=False)
    tech_certificate_name = models.CharField(
        'Technical Certificate Name', max_length=300)
    tech_certi = models.FileField('Technical Certificate', blank=False)
    UAN_number = models.CharField('UAN Number', max_length=200)
    is_employee = models.BooleanField(
        'Is Supervisor is Employee of Elite Works')

    def __str__(self):
        return self.username + "|" + self.name

    class Meta:
        verbose_name = 'Supervisors List'
        verbose_name_plural = 'Supervisors List'


class labourSkillType(models.Model):
    skill_type = models.CharField(
        'Labour Skill Type', max_length=50, null=True)
    skill_type_amount = models.CharField(
        'Skill Type Amount', max_length=50, null=True)

    def __str__(self):
        return self.skill_type

    class Meta:
        verbose_name = 'Labour Skill Type'
        verbose_name_plural = 'Labour Skill Type'


class labourDesignation(models.Model):
    designation = models.CharField(
        'Labour Designation', max_length=50, null=True)

    def __str__(self):
        return self.designation

    class Meta:
        verbose_name = 'Labour Designation'
        verbose_name_plural = 'Labour Designation'


class labour(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, null=True)
    designation = models.ForeignKey(labourDesignation,
                                    verbose_name='Labour Designation', on_delete=models.SET_NULL, null=True)
    skill_type = models.ForeignKey(labourSkillType,
                                   verbose_name='Labour Skill Type', on_delete=models.SET_NULL, null=True)
    name = models.CharField('Labour Name', max_length=250, blank=False)
    dateofbirth = models.DateField('Date of Birth', default=timezone.now)
    image = models.FileField('Labour Profile Picture', blank=True, null=True)
    mobile_number = models.CharField('Mobile Number', max_length=15)
    alter_number = models.CharField(
        'Alternate Number', max_length=15, blank=True, null=True)
    address = models.CharField('Address', max_length=400)
    resume = models.FileField(blank=True, null=True)
    aadhar_number = models.CharField('Aadhar Number', max_length=20)
    aadhar_photo = models.FileField(
        'Aadhar Card Photo', blank=True)
    pan_number = models.CharField(
        'PAN Number', max_length=20, blank=True, null=True)
    pan_photo = models.FileField(
        'PAN Card Photo', blank=True, null=True)
    highest_qual = models.CharField('Highest Qualifications', max_length=200)
    highest_qual_photo = models.FileField(
        'Proof of Highest Qualification', blank=True, null=True)
    ten_certi = models.FileField(
        '10th Certificate Upload', blank=True, null=True)
    twelve_certi = models.FileField(
        '12th Certificate Upload', blank=True, null=True)
    tech_certificate_name = models.CharField(
        'Technical Certificate Name', max_length=300, blank=True, null=True)
    tech_certi = models.FileField(
        'Technical Certificate Upload', blank=True)
    UAN_number = models.CharField('UAN Number', max_length=200, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Labour List'
        verbose_name_plural = 'Labour List'


class Attendance(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    date = models.DateField('Start Date', default=timezone.now)
    labour = models.ForeignKey(labour, on_delete=models.CASCADE)
    A = 'A'
    B = 'B'
    C = 'C'
    R = 'R'
    status = [(A, 'A'), (B, 'B'), (C, 'C'), (R, 'R')]
    shift = models.CharField('Shift', max_length=10,
                             choices=status, default=None)

    def __str__(self):
        return str(self.labour)

    class Meta:
        verbose_name = 'Attandance'
        verbose_name_plural = 'Attandance'
