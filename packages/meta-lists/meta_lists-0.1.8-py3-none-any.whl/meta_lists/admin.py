from django.contrib import admin
from edc_list_data.admin import ListModelAdminMixin

from .admin_site import meta_lists_admin
from .models import (
    Symptoms,
    ArvRegimens,
    OffstudyReasons,
    OiProphylaxis,
    BaselineSymptoms,
    DiabetesSymptoms,
)


@admin.register(Symptoms, site=meta_lists_admin)
class SymptomsAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(ArvRegimens, site=meta_lists_admin)
class ArvRegimensAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(OffstudyReasons, site=meta_lists_admin)
class OffstudyReasonsAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(OiProphylaxis, site=meta_lists_admin)
class OiProphylaxisAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(BaselineSymptoms, site=meta_lists_admin)
class BaselineSymptomsAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(DiabetesSymptoms, site=meta_lists_admin)
class DiabetesSymptomsAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass
