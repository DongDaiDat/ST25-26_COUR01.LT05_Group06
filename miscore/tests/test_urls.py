from django.test import SimpleTestCase
from django.urls import reverse, resolve

from miscore import views


class MiscoreUrlTest(SimpleTestCase):
    def test_root_ui_url_resolves(self):
        url = reverse("root-ui")
        self.assertEqual(resolve(url).func, views.ui_shell)

    def test_api_schools_url_resolves(self):
        url = reverse("api-schools")
        self.assertEqual(resolve(url).func, views.api_schools)

    def test_api_faculties_url_resolves(self):
        url = reverse("api-faculties")
        self.assertEqual(resolve(url).func, views.api_faculties)

    def test_api_lecturers_url_resolves(self):
        url = reverse("api-lecturers")
        self.assertEqual(resolve(url).func, views.api_lecturers)

    def test_api_majors_url_resolves(self):
        url = reverse("api-majors")
        self.assertEqual(resolve(url).func, views.api_majors)

    def test_api_courses_url_resolves(self):
        url = reverse("api-courses")
        self.assertEqual(resolve(url).func, views.api_courses)

    def test_api_curricula_url_resolves(self):
        url = reverse("api_curricula")
        self.assertEqual(resolve(url).func, views.api_curricula)

    def test_api_curriculum_items_url_resolves(self):
        url = reverse("api_curriculum_items")
        self.assertEqual(resolve(url).func, views.api_curriculum_items)

    def test_api_curriculum_relations_url_resolves(self):
        url = reverse("api_curriculum_relations")
        self.assertEqual(resolve(url).func, views.api_curriculum_relations)

    def test_api_tuitions_url_resolves(self):
        url = reverse("api_tuitions")
        self.assertEqual(resolve(url).func, views.api_tuitions)

    def test_api_me_url_resolves(self):
        url = reverse("api_me")
        self.assertEqual(resolve(url).func, views.api_me)

    def test_api_whoami_url_resolves(self):
        url = reverse("api_whoami")
        self.assertEqual(resolve(url).func, views.api_whoami)

    def test_curriculum_pdf_url_resolves(self):
        url = reverse("ui_curriculum_pdf")
        self.assertEqual(resolve(url).func, views.ui_export_curriculum_pdf)