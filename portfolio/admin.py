from django.contrib import admin

from .models import (
    ContactLink,
    Education,
    Experience,
    Profile,
    Project,
    Skill,
)

admin.site.register(ContactLink)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Profile)
admin.site.register(Project)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "is_active", "display_order")
    search_fields = ("name",)
    list_filter = ("is_active",)
    list_editable = ("level", "is_active", "display_order")
