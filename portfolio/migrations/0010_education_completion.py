from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models


def copy_completion_dates(apps, schema_editor):
    Education = apps.get_model("portfolio", "Education")
    records = Education.objects.using(schema_editor.connection.alias)
    if records.filter(end_date__isnull=True).exists():
        raise ValueError("Koulutusten päättymispäivät on täydennettävä ennen migraatiota.")
    for education in records.all():
        education.completion_year = education.end_date.year
        education.completion_month = education.end_date.month
        education.save(using=schema_editor.connection.alias,
                       update_fields=["completion_year", "completion_month"])


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0009_profile_cv_file")]

    operations = [
        migrations.AddField(
            model_name="education", name="education_type",
            field=models.CharField(choices=[("degree", "Tutkinto"), ("course", "Kurssi")],
                                   default="degree", max_length=10, verbose_name="Koulutuksen tyyppi"),
        ),
        migrations.AddField(
            model_name="education", name="completion_year",
            field=models.PositiveSmallIntegerField(null=True, verbose_name="Valmistumisvuosi",
                validators=[MinValueValidator(1900), MaxValueValidator(9999)]),
        ),
        migrations.AddField(
            model_name="education", name="completion_month",
            field=models.PositiveSmallIntegerField(blank=True, null=True,
                choices=[(month, f"{month:02d}") for month in range(1, 13)],
                help_text="Jätä tyhjäksi, jos tiedät vain vuoden.", verbose_name="Valmistumiskuukausi"),
        ),
        migrations.RunPython(copy_completion_dates),
        migrations.AlterField(
            model_name="education", name="completion_year",
            field=models.PositiveSmallIntegerField(verbose_name="Valmistumisvuosi",
                validators=[MinValueValidator(1900), MaxValueValidator(9999)]),
        ),
        migrations.AlterModelOptions(name="education", options={
            "ordering": ["display_order", "-completion_year", "-completion_month"],
        }),
        migrations.RemoveField(model_name="education", name="start_date"),
        migrations.RemoveField(model_name="education", name="end_date"),
    ]
