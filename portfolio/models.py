from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Skill(models.Model):
    """Tallentaa yhden CV-sivustolla näytettävän taidon."""

    name = models.CharField(max_length=100)
    level = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name


class Profile(models.Model):
    """Tallentaa yhden CV-sivustolla näytettävän profiilin."""

    full_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    bio = models.TextField()
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to="profile/", blank=True)
    image_alt_text = models.CharField(max_length=150, blank=True, default="")

    def __str__(self):
        return self.full_name


class Experience(models.Model):
    """Malli työkokemusten ja työhistorian tallentamiseen."""

    company = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "-start_date"]

    def __str__(self):
        return f"{self.job_title} - {self.company}"


class Education(models.Model):
    """Malli koulutuksen tallentamiseen."""

    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "-start_date"]

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class Project(models.Model):
    """Tallentaa yhden CV-sivustolla esiteltävän projektin."""

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    technologies = models.CharField(max_length=200, blank=True)
    project_url = models.URLField(blank=True)
    source_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-is_featured", "display_order", "title"]

    def __str__(self):
        return self.title


class ContactLink(models.Model):
    """Malli sosiaalisen median linkkien ja yhteystietolinkkien tallentamiseen."""

    label = models.CharField(max_length=50)
    url = models.CharField(max_length=300)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "label"]

    def __str__(self):
        return self.label
