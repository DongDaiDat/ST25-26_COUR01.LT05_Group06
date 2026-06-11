from decimal import Decimal

from miscore.models import (
    University,
    School,
    Faculty,
    Major,
    Course,
    Curriculum,
    ListCourse,
)


def create_base_data():
    university = University.objects.create(
        name="Phenikaa University",
        is_active=True,
    )

    school = School.objects.create(
        university=university,
        name="Trường Công nghệ thông tin",
        is_active=True,
    )

    faculty = Faculty.objects.create(
        school=school,
        code="cntt",
        name="Khoa Công nghệ thông tin",
        is_active=True,
    )

    major = Major.objects.create(
        faculty=faculty,
        code="SE",
        name="Kỹ thuật phần mềm",
        is_active=True,
    )

    curriculum = Curriculum.objects.create(
        major=major,
        faculty=faculty,
        year=2025,
    )

    course_1 = Course.objects.create(
        code="INT101",
        name="Nhập môn lập trình",
        credits=Decimal("3.0"),
        credits_lt=Decimal("2.0"),
        credits_th=Decimal("1.0"),
        faculty=faculty,
        is_active=True,
    )

    course_2 = Course.objects.create(
        code="INT102",
        name="Cơ sở dữ liệu",
        credits=Decimal("3.0"),
        credits_lt=Decimal("2.0"),
        credits_th=Decimal("1.0"),
        faculty=faculty,
        is_active=True,
    )

    list_course_1 = ListCourse.objects.create(
        curriculum=curriculum,
        course=course_1,
        semester_no=1,
        requirement_type=ListCourse.RequirementType.COMPULSORY,
        is_active=True,
    )

    list_course_2 = ListCourse.objects.create(
        curriculum=curriculum,
        course=course_2,
        semester_no=2,
        requirement_type=ListCourse.RequirementType.ELECTIVE,
        is_active=False,
    )

    return {
        "university": university,
        "school": school,
        "faculty": faculty,
        "major": major,
        "curriculum": curriculum,
        "course_1": course_1,
        "course_2": course_2,
        "list_course_1": list_course_1,
        "list_course_2": list_course_2,
    }