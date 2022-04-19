from django.contrib import admin
from .models import *


@admin.register(Formation)
class FormationManager(admin.ModelAdmin):
    list_display = ['president', 'fromDate', 'toDate', 'teacher']


@admin.register(Deplomat)
class DeplomatManager(admin.ModelAdmin):
    list_display = ['student_name', 'serial_num']


admin.site.register(UnassActivite)
admin.site.register(Activite)
admin.site.register(CaralogueFormation)
admin.site.register(AnetmentUnass)
admin.site.register(ChooseUsReasons)
admin.site.register(WhyChoosingUs)
admin.site.register(TeamMember)
admin.site.register(MessagesFromNewClients)
admin.site.register(OurContactInfo)
