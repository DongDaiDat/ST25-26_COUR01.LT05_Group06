from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from miscore.models import (
    Faculty,
    Major,
    Lecturer,
    Course,
    Curriculum,
    ListCourse,
    Tuition,
)
from miscore.tests.utils import create_base_data


class FacultyModelTest(TestCase):
    def test_faculty_code_is_converted_to_uppercase_when_saved(self):
        data = create_base_data()
        faculty = data["faculty"]

        self.assertEqual(faculty.code, "CNTT")

    def test_faculty_string_representation_returns_name(self):
        data = create_base_data()
        faculty = data["faculty"]

        self.assertEqual(str(faculty), "Khoa Công nghệ thông tin")


class MajorModelTest(TestCase):
    def test_major_school_is_synced_from_faculty_when_saved(self):
        data = create_base_data()
        major = data["major"]
        faculty = data["faculty"]

        self.assertEqual(major.school, faculty.school)

    def test_major_string_representation_returns_name(self):
        data = create_base_data()
        major = data["major"]

        self.assertEqual(str(major), "Kỹ thuật phần mềm")


class LecturerModelTest(TestCase):
    def test_lecturer_school_is_synced_from_faculty_when_saved(self):
        data = create_base_data()
        faculty = data["faculty"]

        lecturer = Lecturer.objects.create(
            faculty=faculty,
            name="Nguyễn Văn A",
            position="Giảng viên",
            email="a@example.com",
            phone="0123456789",
            is_active=True,
        )

        self.assertEqual(lecturer.school, faculty.school)

    def test_lecturer_string_representation_returns_name(self):
        data = create_base_data()
        faculty = data["faculty"]

        lecturer = Lecturer.objects.create(
            faculty=faculty,
            name="Nguyễn Văn A",
        )

        self.assertEqual(str(lecturer), "Nguyễn Văn A")


class CourseModelTest(TestCase):
    def test_create_valid_course_successfully(self):
        data = create_base_data()
        course = data["course_1"]

        self.assertEqual(course.code, "INT101")
        self.assertEqual(course.name, "Nhập môn lập trình")
        self.assertEqual(course.credits, Decimal("3.0"))

    def test_course_string_representation(self):
        data = create_base_data()
        course = data["course_1"]

        self.assertEqual(str(course), "INT101 — Nhập môn lập trình")

    def test_course_accepts_half_step_credit(self):
        data = create_base_data()
        faculty = data["faculty"]

        course = Course(
            code="INT103",
            name="Kiểm thử phần mềm",
            credits=Decimal("2.5"),
            credits_lt=Decimal("1.5"),
            credits_th=Decimal("1.0"),
            faculty=faculty,
        )

        course.full_clean()

    def test_course_rejects_credit_not_half_step(self):
        data = create_base_data()
        faculty = data["faculty"]

        course = Course(
            code="INT104",
            name="Trí tuệ nhân tạo",
            credits=Decimal("3.2"),
            credits_lt=Decimal("2.0"),
            credits_th=Decimal("1.2"),
            faculty=faculty,
        )

        with self.assertRaises(ValidationError):
            course.full_clean()

    def test_course_rejects_negative_credit(self):
        data = create_base_data()
        faculty = data["faculty"]

        course = Course(
            code="INT105",
            name="Môn học lỗi",
            credits=Decimal("-1.0"),
            credits_lt=Decimal("0.0"),
            credits_th=Decimal("-1.0"),
            faculty=faculty,
        )

        with self.assertRaises(ValidationError):
            course.full_clean()

    def test_course_rejects_credit_less_than_minimum(self):
        data = create_base_data()
        faculty = data["faculty"]

        course = Course(
            code="INT106",
            name="Môn học không hợp lệ",
            credits=Decimal("0.0"),
            credits_lt=Decimal("0.0"),
            credits_th=Decimal("0.0"),
            faculty=faculty,
        )

        with self.assertRaises(ValidationError):
            course.full_clean()

    def test_course_rejects_when_total_credit_not_equal_lt_plus_th(self):
        data = create_base_data()
        faculty = data["faculty"]

        course = Course(
            code="INT107",
            name="Môn học sai tổng tín",
            credits=Decimal("3.0"),
            credits_lt=Decimal("1.0"),
            credits_th=Decimal("1.0"),
            faculty=faculty,
        )

        with self.assertRaises(ValidationError):
            course.full_clean()


class CurriculumModelTest(TestCase):
    def test_curriculum_faculty_is_synced_from_major_when_saved(self):
        data = create_base_data()
        curriculum = data["curriculum"]
        major = data["major"]

        self.assertEqual(curriculum.faculty, major.faculty)

    def test_curriculum_string_representation(self):
        data = create_base_data()
        curriculum = data["curriculum"]

        self.assertEqual(str(curriculum), "Kỹ thuật phần mềm — 2025")


class TuitionModelTest(TestCase):
    def test_calc_total_credits_only_counts_active_list_courses(self):
        data = create_base_data()
        curriculum = data["curriculum"]

        total = Tuition.calc_total_credits(curriculum)

        self.assertEqual(total, Decimal("3.0"))

    def test_recalc_updates_total_credits_and_total_amount(self):
        data = create_base_data()
        curriculum = data["curriculum"]

        tuition = Tuition.objects.create(
            curriculum=curriculum,
            price_per_credit=Decimal("1000000.00"),
        )

        tuition.recalc()

        self.assertEqual(tuition.total_credits, Decimal("3.0"))
        self.assertEqual(tuition.total_amount, Decimal("3000000.00"))


class ListCourseModelTest(TestCase):
    def test_list_course_string_representation(self):
        data = create_base_data()
        list_course = data["list_course_1"]

        self.assertIn("INT101", str(list_course))
        self.assertIn("Kỹ thuật phần mềm", str(list_course))