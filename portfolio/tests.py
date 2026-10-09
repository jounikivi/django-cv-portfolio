from django.test import SimpleTestCase
from django.template.loader import render_to_string
from datetime import date

from .models import Skill, Profile, Experience, Education, Project, ContactLink
from .views import group_skills


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
