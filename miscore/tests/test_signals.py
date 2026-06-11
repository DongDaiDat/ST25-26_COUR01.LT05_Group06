from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from miscore.models import (
    Course,
    ListCourse,
    Profile,
    Tuition,
)
from miscore.tests.utils import create_base_data


class UserProfileSignalTest(TestCase):
    def test_profile_is_created_automatically_when_user_is_created(self):
        user = User.objects.create_user(
            username="student_signal",
            password="123456",
        )

        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_profile_is_created_if_missing_when_user_is_saved_again(self):
        user = User.objects.create_user(
            username="missing_profile",
            password="123456",
        )

        Profile.objects.filter(user=user).delete()

        user.first_name = "Test"
        user.save()

        self.assertTrue(Profile.objects.filter(user=user).exists())


class TuitionSignalTest(TestCase):
    def test_tuition_is_recalculated_when_listcourse_is_created(self):
        data = create_base_data()
        curriculum = data["curriculum"]
        faculty = data["faculty"]

        tuition = Tuition.objects.create(
            curriculum=curriculum,
            price_per_credit=Decimal("1000000.00"),
        )

        self.assertEqual(tuition.total_credits, Decimal("3.0"))

        course_3 = Course.objects.create(
            code="INT103",
            name="Kiểm thử phần mềm",
            credits=Decimal("2.0"),
            credits_lt=Decimal("1.0"),
            credits_th=Decimal("1.0"),
            faculty=faculty,
            is_active=True,
        )

        ListCourse.objects.create(
            curriculum=curriculum,
            course=course_3,
            semester_no=3,
            requirement_type=ListCourse.RequirementType.COMPULSORY,
            is_active=True,
        )

        tuition.refresh_from_db()

        self.assertEqual(tuition.total_credits, Decimal("5.0"))
        self.assertEqual(tuition.total_amount, Decimal("5000000.00"))

    def test_tuition_is_recalculated_when_listcourse_is_deleted(self):
        data = create_base_data()
        curriculum = data["curriculum"]
        list_course = data["list_course_1"]

        tuition = Tuition.objects.create(
            curriculum=curriculum,
            price_per_credit=Decimal("1000000.00"),
        )

        self.assertEqual(tuition.total_credits, Decimal("3.0"))

        list_course.delete()

        tuition.refresh_from_db()

        self.assertEqual(tuition.total_credits, Decimal("0"))
        self.assertEqual(tuition.total_amount, Decimal("0.00"))