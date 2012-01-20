from django.contrib import admin
from models import Invitation, InvitationRequest, InvitationStats


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'expiration_date')
admin.site.register(Invitation, InvitationAdmin)


class InvitationRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_requested')
admin.site.register(InvitationRequest, InvitationRequestAdmin)


class InvitationStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'available', 'sent', 'accepted', 'performance')

    def performance(self, obj):
        return '%0.2f' % obj.performance
admin.site.register(InvitationStats, InvitationStatsAdmin)
