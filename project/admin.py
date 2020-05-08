from django.contrib import admin
from project.models import *
# Register your models here.

admin.site.site_header = 'Elite Works - Master Panel'


class InlineContractors(admin.TabularInline):
    model = otherContractors
    extra = 1


class TenderAdmin(admin.ModelAdmin):

    inlines = [InlineContractors]

    list_display = (
        'tender_number',
        'date_created',
        'tender_name',
        'tender_submission_date',
        'tech_bid_opening_date',
        'bid_status',
        'prize_bid',
    )
    list_filter = (
        'tender_submission_date',
        'physical_submission_date',
        'tech_bid_opening_date',
        'bid_status',
        'prize_bid',
    )
    search_fields = (
        'tender_submission_date',
        'physical_submission_date',
        'tech_bid_opening_date',
        'bid_status',
        'prize_bid',
    )


admin.site.register(Tender, TenderAdmin)
admin.site.register(otherContractors)
admin.site.register(Security_Deposit)
admin.site.register(Projects)
admin.site.register(ProjectStart)
admin.site.register(ProjectRepeter)
admin.site.register(ProjectFollowup)
