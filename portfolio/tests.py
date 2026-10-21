from django.test import SimpleTestCase, TestCase
from django.template.loader import render_to_string
from datetime import date

from .models import Skill, Profile, Experience, Education, Project, ContactLink
from .views import group_skills


class PresentationUpdateTests(TestCase):
    def test_content_seed_preserves_admin_edits_and_existing_cv_data(self):
        from importlib import import_module
        from types import SimpleNamespace
        from django.apps import apps
        from django.db import connection

        profile = Profile.objects.create(full_name="Jouni Kiviperä", bio="Oma esittely",
                                         headline="Adminissa muokattu otsikko", cv_file="documents/oma.pdf")
        experience = Experience.objects.create(company="Jimm’s PC-Store Oy", job_title="Harjoittelija",
                                               start_date=date(2024, 4, 1), description="Oma kuvaus")
        seed = import_module("portfolio.migrations.0012_initial_presentation_content").seed_presentation
        seed(apps, SimpleNamespace(connection=connection))
        profile.refresh_from_db()
        experience.refresh_from_db()
        self.assertEqual(profile.headline, "Adminissa muokattu otsikko")
        self.assertEqual(profile.bio, "Oma esittely")
        self.assertEqual(profile.cv_file.name, "documents/oma.pdf")
        self.assertTrue(profile.about_text)
        self.assertEqual(experience.job_title, "Harjoittelija")
        self.assertEqual(experience.description, "Oma kuvaus")
        self.assertIn("kokoonpano", experience.display_title)

    def test_optional_presentation_fields_are_escaped_and_can_be_hidden(self):
        profile = Profile.objects.create(full_name="Testi", about_text="<script>alert(1)</script>")
        response = self.client.get("/")
        self.assertContains(response, 'href="#about"')
        self.assertContains(response, "&lt;script&gt;")
        self.assertNotContains(response, "<script>alert(1)</script>")
        profile.about_text = ""
        profile.save()
        self.assertNotContains(self.client.get("/"), 'href="#about"')

    def test_custom_skill_descriptions_survive_grouping(self):
        groups = group_skills([Skill(name="Linux", description="Oma käytännön esimerkki")])
        self.assertEqual(groups[0]["descriptions"], ["Oma käytännön esimerkki"])


class SkillGroupingTests(SimpleTestCase):
    def test_current_skills_form_four_groups_without_losing_skills(self):
        names = [
            "IT-tuki ja käyttäjäneuvonta", "Windows ja tekninen ongelmanratkaisu",
            "Tietokoneiden kokoonpano ja testaus", "Python- ja Django-kehitys",
            "SQL ja SQLite", "React ja TypeScript",
            "Ohjelmistojen ja käyttöliittymien testaus", "Git ja GitHub",
        ]
        groups = group_skills([Skill(name=name) for name in names])
        self.assertEqual(len(groups), 4)
        self.assertCountEqual([item for group in groups for item in group["items"]], names)

    def test_new_or_renamed_skill_remains_visible(self):
        self.assertEqual(group_skills([Skill(name="Linux")]), [
            {"title": "Muu osaaminen", "items": ["Linux"]},
        ])

    def test_empty_groups_are_hidden(self):
        self.assertEqual(group_skills([]), [])
        self.assertEqual(len(group_skills([Skill(name="Git ja GitHub")])), 1)


class PortfolioTemplateTests(SimpleTestCase):
    def test_contact_icons_download_and_oraowl_logo(self):
        html = render_to_string("portfolio/home.html", {
            "profile": Profile(full_name="Testaaja", cv_file="documents/cv.pdf"),
            "projects": [Project(title="ORAOwl"), Project(title="Toinen")],
            "contact_links": [
                ContactLink(label="Sähköposti", url="mailto:test@example.com"),
                ContactLink(label="Puhelin", url="tel:+358401234567"),
                ContactLink(label="GitHub", url="https://github.com/test"),
                ContactLink(label="LinkedIn", url="https://www.linkedin.com/in/test"),
                ContactLink(label="Muu", url="https://example.com"),
            ],
        })
        for name in ("mail", "phone", "github", "linkedin", "download"):
            self.assertIn(f'class="icon icon--{name}"', html)
        self.assertEqual(html.count('class="project-logo"'), 1)
        self.assertIn('aria-hidden="true" focusable="false"', html)
        self.assertIn('class="contact-label">Muu</span>', html)

    def test_empty_page_renders(self):
        html = render_to_string("portfolio/home.html", {})
        self.assertIn('id="contact"', html)
        self.assertIn("Osaamisia lisätään myöhemmin.", html)
        self.assertNotIn('class="profile-image"', html)
        self.assertNotIn("Lataa CV", html)

    def test_sections_render_optional_data_and_links(self):
        html = render_to_string("portfolio/home.html", {
            "profile": Profile(full_name="Testaaja", location="Turku"),
            "experiences": [Experience(company="Yritys", job_title="Kehittäjä",
                                       start_date=date(2025, 1, 1))],
            "educations": [Education(degree="Kurssi", education_type="course",
                                      completion_year=2024)],
            "projects": [Project(title="Esimerkki", is_featured=True,
                                  source_url="https://example.com/source")],
            "contact_links": [ContactLink(label="Sähköposti", url="mailto:test@example.com")],
        })
        self.assertIn("nykyinen", html)
        self.assertIn("Suoritettu 2024", html)
        self.assertIn("project-card--featured", html)
        self.assertIn('href="https://example.com/source"', html)
        self.assertIn('class="contact-primary"', html)
        self.assertNotIn("Etunimi Sukunimi", html)
