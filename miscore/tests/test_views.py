from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from miscore.models import Profile
from miscore.tests.utils import create_base_data


class UiShellViewTest(TestCase):
    def test_ui_shell_returns_html(self):
        response = self.client.get(reverse("root-ui"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Education Management")
        self.assertContains(response, "mis-ui/app.js")


class ApiSchoolViewTest(TestCase):
    def test_api_schools_returns_items(self):
        create_base_data()

        response = self.client.get(reverse("api-schools"))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("items", data)
        self.assertEqual(len(data["items"]), 1)
        self.assertEqual(data["items"][0]["name"], "Trường Công nghệ thông tin")

    def test_api_schools_filters_by_query(self):
        create_base_data()

        response = self.client.get(reverse("api-schools"), {"q": "Công nghệ"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["items"]), 1)


class ApiFacultyViewTest(TestCase):
    def test_api_faculties_returns_items(self):
        create_base_data()

        response = self.client.get(reverse("api-faculties"))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("items", data)
        self.assertEqual(data["items"][0]["code"], "CNTT")

    def test_api_faculties_order_by_code(self):
        create_base_data()

        response = self.client.get(reverse("api-faculties"), {"order": "code"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("items", data)


class ApiMajorViewTest(TestCase):
    def test_api_majors_returns_items(self):
        create_base_data()

        response = self.client.get(reverse("api-majors"))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("items", data)
        self.assertEqual(data["items"][0]["code"], "SE")

    def test_api_majors_filters_by_query(self):
        create_base_data()

        response = self.client.get(reverse("api-majors"), {"q": "phần mềm"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["items"]), 1)


class ApiCourseViewTest(TestCase):
    def test_api_courses_returns_items(self):
        create_base_data()

        response = self.client.get(reverse("api-courses"))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("items", data)
        self.assertEqual(len(data["items"]), 2)
        self.assertEqual(data["items"][0]["code"], "INT101")

    def test_api_courses_filters_by_query(self):
        create_base_data()

        response = self.client.get(reverse("api-courses"), {"q": "Cơ sở"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["items"]), 1)
        self.assertEqual(data["items"][0]["code"], "INT102")

    def test_api_courses_order_descending_by_code(self):
        create_base_data()

        response = self.client.get(reverse("api-courses"), {"order": "-code"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["items"][0]["code"], "INT102")


class ApiCurriculumViewTest(TestCase):
    def test_api_curricula_returns_items(self):
        create_base_data()

        response = self.client.get(reverse("api_curricula"))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("items", data)
        self.assertEqual(data["items"][0]["major"], "Kỹ thuật phần mềm")
        self.assertEqual(data["items"][0]["year"], 2025)


class ApiCurriculumItemsViewTest(TestCase):
    def test_api_curriculum_items_missing_cur_returns_404(self):
        response = self.client.get(reverse("api_curriculum_items"))

        self.assertEqual(response.status_code, 404)

    def test_api_curriculum_items_invalid_cur_returns_404(self):
        response = self.client.get(reverse("api_curriculum_items"), {"cur": 9999})

        self.assertEqual(response.status_code, 404)

    def test_api_curriculum_items_returns_items(self):
        data = create_base_data()
        curriculum = data["curriculum"]

        response = self.client.get(
            reverse("api_curriculum_items"),
            {"cur": curriculum.id},
        )

        self.assertEqual(response.status_code, 200)
        result = response.json()

        self.assertTrue(result["ok"])
        self.assertEqual(result["info"]["major"], "Kỹ thuật phần mềm")
        self.assertEqual(len(result["items"]), 2)

    def test_api_curriculum_items_filters_active_only(self):
        data = create_base_data()
        curriculum = data["curriculum"]

        response = self.client.get(
            reverse("api_curriculum_items"),
            {
                "cur": curriculum.id,
                "active": "1",
            },
        )

        self.assertEqual(response.status_code, 200)
        result = response.json()

        self.assertEqual(len(result["items"]), 1)
        self.assertEqual(result["items"][0]["code"], "INT101")
        self.assertEqual(result["info"]["total_active_credits"], 3.0)

    def test_api_curriculum_items_filters_by_semester(self):
        data = create_base_data()
        curriculum = data["curriculum"]

        response = self.client.get(
            reverse("api_curriculum_items"),
            {
                "cur": curriculum.id,
                "sem": "2",
            },
        )

        self.assertEqual(response.status_code, 200)
        result = response.json()

        self.assertEqual(len(result["items"]), 1)
        self.assertEqual(result["items"][0]["code"], "INT102")

    def test_api_curriculum_items_ignores_invalid_semester(self):
        data = create_base_data()
        curriculum = data["curriculum"]

        response = self.client.get(
            reverse("api_curriculum_items"),
            {
                "cur": curriculum.id,
                "sem": "abc",
            },
        )

        self.assertEqual(response.status_code, 200)
        result = response.json()

        self.assertEqual(len(result["items"]), 2)

    def test_api_curriculum_items_filters_by_requirement_type(self):
        data = create_base_data()
        curriculum = data["curriculum"]

        response = self.client.get(
            reverse("api_curriculum_items"),
            {
                "cur": curriculum.id,
                "type": "COMPULSORY",
            },
        )

        self.assertEqual(response.status_code, 200)
        result = response.json()

        self.assertEqual(len(result["items"]), 1)
        self.assertEqual(result["items"][0]["requirement_label"], "Bắt buộc")


class ApiTuitionViewTest(TestCase):
    def test_api_tuitions_returns_items(self):
        from decimal import Decimal
        from miscore.models import Tuition

        data = create_base_data()
        curriculum = data["curriculum"]

        Tuition.objects.create(
            curriculum=curriculum,
            price_per_credit=Decimal("1000000.00"),
            note="Học phí CTĐT 2025",
        )

        response = self.client.get(reverse("api_tuitions"))

        self.assertEqual(response.status_code, 200)
        result = response.json()

        self.assertIn("items", result)
        self.assertEqual(len(result["items"]), 1)
        self.assertEqual(result["items"][0]["total_credits"], 3.0)
        self.assertEqual(result["items"][0]["total_amount"], 3000000.0)

    def test_api_tuitions_filters_by_query(self):
        from decimal import Decimal
        from miscore.models import Tuition

        data = create_base_data()
        curriculum = data["curriculum"]

        Tuition.objects.create(
            curriculum=curriculum,
            price_per_credit=Decimal("1000000.00"),
            note="Học phí CTĐT 2025",
        )

        response = self.client.get(reverse("api_tuitions"), {"q": "2025"})

        self.assertEqual(response.status_code, 200)
        result = response.json()

        self.assertEqual(len(result["items"]), 1)


class ApiUserViewTest(TestCase):
    def test_api_me_returns_not_authenticated_when_anonymous(self):
        response = self.client.get(reverse("api_me"))

        self.assertEqual(response.status_code, 200)
        result = response.json()

        self.assertTrue(result["ok"])
        self.assertFalse(result["is_auth"])

    def test_api_me_returns_authenticated_user_info(self):
        user = User.objects.create_user(
            username="student01",
            password="123456",
            email="student01@example.com",
        )

        Profile.objects.filter(user=user).update(role=Profile.Role.STUDENT)

        self.client.login(username="student01", password="123456")
        response = self.client.get(reverse("api_me"))

        self.assertEqual(response.status_code, 200)
        result = response.json()

        self.assertTrue(result["ok"])
        self.assertTrue(result["is_auth"])
        self.assertEqual(result["username"], "student01")
        self.assertEqual(result["role"], "STUDENT")

    def test_api_whoami_returns_none_when_anonymous(self):
        response = self.client.get(reverse("api_whoami"))

        self.assertEqual(response.status_code, 200)
        result = response.json()

        self.assertFalse(result["ok"])
        self.assertIsNone(result["user"])

    def test_api_whoami_returns_user_when_authenticated(self):
        user = User.objects.create_user(
            username="staff01",
            password="123456",
            email="staff01@example.com",
            is_staff=True,
        )

        Profile.objects.filter(user=user).update(role=Profile.Role.STAFF)

        self.client.login(username="staff01", password="123456")
        response = self.client.get(reverse("api_whoami"))

        self.assertEqual(response.status_code, 200)
        result = response.json()

        self.assertTrue(result["ok"])
        self.assertEqual(result["user"]["username"], "staff01")
        self.assertEqual(result["user"]["role"], "STAFF")