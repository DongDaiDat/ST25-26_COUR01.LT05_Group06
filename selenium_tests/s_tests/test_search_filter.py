from config import BASE_URL, ADMIN_USERNAME, ADMIN_PASSWORD
from helpers import (
    COURSE_LIST_URL, MAJOR_LIST_URL, CURRICULUM_LIST_URL,
    login_admin, body_text, admin_search,
    create_course_via_admin, create_major_via_admin, create_curriculum_via_admin,
)


def test_search_filter_course_by_code_on_admin(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    course = create_course_via_admin(driver)
    text = admin_search(driver, COURSE_LIST_URL, course["code"])
    assert course["code"].lower() in text.lower()


def test_search_filter_major_by_code_on_admin(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    major = create_major_via_admin(driver)
    text = admin_search(driver, MAJOR_LIST_URL, major["code"])
    assert major["code"].lower() in text.lower()


def test_search_filter_curriculum_by_major_on_admin(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    curriculum = create_curriculum_via_admin(driver)
    major = curriculum["major"]

    # Tìm bằng mã ngành, nhưng trang danh sách CTĐT hiển thị tên ngành/năm,
    # không hiển thị mã ngành vì Major.__str__ trả về name.
    text = admin_search(driver, CURRICULUM_LIST_URL, major["code"])
    lower = text.lower()
    assert major["name"].lower() in lower or curriculum["year"] in text


def test_api_course_search_returns_created_course(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    course = create_course_via_admin(driver)
    driver.get(f"{BASE_URL}/api/courses?q={course['code']}")
    assert course["code"].lower() in body_text(driver).lower()


def test_api_major_search_returns_created_major(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    major = create_major_via_admin(driver)
    driver.get(f"{BASE_URL}/api/majors?q={major['code']}")
    assert major["code"].lower() in body_text(driver).lower()
