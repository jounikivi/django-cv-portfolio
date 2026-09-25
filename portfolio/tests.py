from django.test import SimpleTestCase

from .models import Skill
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
