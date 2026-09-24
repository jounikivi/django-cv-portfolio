from django.contrib import admin

from .models import (
    ContactLink,
    Education,
    Experience,
    Profile,
    Project,
    Skill,
)


@admin.register(ContactLink)
class ContactLinkAdmin(admin.ModelAdmin):
    list_display = ("label", "url", "is_active", "display_order")
    search_fields = ("label", "url")
    list_filter = ("is_active",)
    list_editable = ("is_active", "display_order")


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = (
        "degree",
        "institution",
        "field_of_study",
        "education_type",
        "completion_year",
        "completion_month",
        "is_active",
        "display_order",
    )
    search_fields = ("degree", "institution", "field_of_study", "description")
    list_filter = ("is_active",)
    list_editable = ("is_active", "display_order")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "job_title",
        "company",
        "start_date",
        "end_date",
        "is_active",
        "display_order",
    )
    search_fields = ("job_title", "company", "description")
    list_filter = ("is_active",)
    list_editable = ("is_active", "display_order")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "title", "location")
    search_fields = ("full_name", "title", "location")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "technologies",
        "is_featured",
        "is_active",
        "display_order",
    )
    search_fields = ("title", "description", "technologies")
    list_filter = ("is_featured", "is_active")
    list_editable = ("is_featured", "is_active", "display_order")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    exclude = ("level",)
    list_display = ("name", "is_active", "display_order")
    search_fields = ("name",)
    list_filter = ("is_active",)
    list_editable = ("is_active", "display_order")
