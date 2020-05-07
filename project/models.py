from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from manpower.models import *

# Create your models here.


class Tender(models.Model):
    Yes = 'Yes'
    No = 'No'
    status = [(Yes, 'Yes'), (No, 'No')]
    uuid_no = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    date_created = models.DateTimeField(
        'Creation Date', auto_now_add=True, null=True)
    tender_number = models.CharField('Tender Number / ID', max_length=500)
    tender_name = models.CharField('Tender Name', max_length=500)
    tender_description = models.TextField('Tender Description')
    tender_submission_date = models.DateField(
        'Tender Submission Date', default=timezone.now)
    tender_purchase_reciept = models.FileField('Tender Purchase Reciept')
    tender_confirmation_reciept = models.FileField(
        'Tender Confirmation Reciept')
    physical_submission_date = models.DateField(
        'Physical Submission Date', default=timezone.now)
    tech_bid_opening_date = models.DateField(
        'Technical Bid Opening Date', default=timezone.now)
    bid_status = models.CharField(
        'Bid Status', max_length=10, choices=status, default=No)
    bid_price_opening_date = models.DateField(
        'Bid price opening date', blank=True, default=timezone.now)
    prize_bid = models.CharField('Bid Price', max_length=50)

    def __str__(self):
        return self.tender_number


class otherContractors(models.Model):
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)
    contructor_name = models.CharField(
        'Contructor Name', max_length=200, blank=False, null=True)
    contructor_location = models.CharField(
        'Contructor Location', max_length=200, blank=False, null=True)
    contact_number = models.CharField(
        'Contact Number', max_length=200, blank=False, null=True)
    email_address = models.EmailField(
        'Email Address', max_length=200, blank=False, null=True)
    other_contructor_bid_amount = models.CharField(
        'Other Contructors Bid Amount', max_length=200, blank=False, null=True)

    def __str__(self):
        return self.contructor_name+"--"+self.tender.tender_name

    class Meta:
        verbose_name = 'Other Contractors'
        verbose_name_plural = 'Other Contractors'


class Projects(models.Model):
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)
    superviser = models.ForeignKey(
        on_delete=models.CASCADE, to='manpower.SuperVisors', null=True)
    project_number = models.CharField(
        'Project Number', max_length=200, blank=False, null=True)
    project_name = models.CharField(
        'Project Name', max_length=200, blank=False, null=True)
    project_start_date = models.DateField(
        'Project Start Date', default=timezone.now)

    def __str__(self):
        return self.tender.tender_number + "-" + self.project_name

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Project'


class Security_Deposit(models.Model):
    DD = 'DD'
    FDR = 'FDR'
    BG = 'BG'
    STATUS = [(DD, 'DD'), (FDR, 'FDR'), (BG, 'BG')]
    deposit_type = models.CharField(
        max_length=10, choices=STATUS, default=None)
    cretion_date = models.DateField('Creation Date', default=timezone.now)
    submission_date = models.DateField('Submission Date', default=timezone.now)
    bank_name = models.CharField(
        'Bank Name', max_length=50, null=True, blank=True)
    amount = models.CharField('Amount', max_length=10, null=True, blank=True)
    validity = models.DateField(
        'Validity', default=timezone.now, null=True, blank=True)
    maturity_amount = models.CharField(
        'Maturity Amount', max_length=50, blank=True)
    support_doc = models.FileField(
        'Supportive Document', null=True, blank=True)

    def __str__(self):
        return self.bank_name + " - " + self.deposit_type

    class Meta:
        verbose_name = 'Security Deposit'
        verbose_name_plural = 'Security Deposit'


class ProjectP1(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, null=True)
    ai_sub_date = models.DateField(
        'Agreement & Indemnity Bond Submission Date', default=timezone.now)
    ai_upload = models.FileField('Agreement & Indemnity Bond Upload')
    security_deposit = models.ForeignKey(
        Security_Deposit, on_delete=models.CASCADE)
    ahtsn = models.CharField(
        'Agreement Handover to Supervisor Name', max_length=50)
    ahts = models.DateField(
        'Agreement Handover to Supervisor Date', default=timezone.now, null=True)
    asd = models.DateField('Agreement Submission Date',
                           default=timezone.now, null=True)
    astdn = models.CharField(
        'Agreement Submission to (Division Name)', max_length=50)
    astpn = models.CharField(
        'Agreement Submission to (Person Name)', max_length=50)

    class Meta:
        verbose_name = 'Project Phase - 1'
        verbose_name_plural = 'Project Phase - 1'

    def __str__(self):
        return self.tender.tender_name+" - "+self.project_name


class ProjectP2(models.Model):
    Assistant = 'Assistant'
    Engineer = 'Engineer'
    Division_Office = 'Division Office'
    Supervisor = 'Supervisor'
    POSITION = [(Assistant, 'Assistant'), (Engineer, 'Engineer'),
                (Division_Office, 'Division Office'), (Supervisor, 'Supervisor')]
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, null=True)
    cover_letter = models.FileField('Covering Letter Copy')
    invoice_copy = models.FileField('Invoice Copy')
    atten_sheet = models.FileField('Attendance Sheet Copy')
    salary_sheet = models.FileField('Salary Sheet Copy')
    bank_statement = models.FileField('Bank Statement Copy')
    epf_chalan = models.FileField('EPF Chalan (Upload)')
    epf_ecr = models.FileField('EPF ECR (Upload)')
    esic_chalan = models.FileField('ESIC Chalan (Upload)')
    esic_ecr = models.FileField('ESIC ECR (Upload)')
    labor_passbook = models.FileField('Labore Passbook / BS (Upload)')
    doc_handover_date = models.DateField(
        'All Document Handover Date', default=timezone.now)
    doc_handover_option = models.CharField(
        'All Document Handover to (Options)', choices=POSITION, max_length=200, default=None)
    doc_handover_person = models.CharField(
        'All Document Handover to (Person Name)', max_length=50, null=True)

    class Meta:
        verbose_name = 'Project Phase - 2'
        verbose_name_plural = 'Project Phase - 2'

    def __str__(self):
        return self.project.project_name+" - "+self.doc_handover_date


class ProjectFollowup(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, null=True)
    date_time = models.DateTimeField(
        'Current Date & Time', auto_now_add=True, null=True)
    followup_by = models.CharField(max_length=200, null=True)
    foolowup_to = models.CharField(max_length=200, null=True)
    foolowup_remarks = models.CharField(max_length=500, null=True)

    class Meta:
        verbose_name = 'Project Followup'
        verbose_name_plural = 'Project Followup'

    def __str__(self):
        return self.project.project_name+" - "+self.foolowup_to


class superdata(models.Model):
    superviser = models.ForeignKey(
        on_delete=models.CASCADE, to='manpower.SuperVisors')
