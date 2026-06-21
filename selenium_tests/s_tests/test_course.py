from config import ADMIN_USERNAME, ADMIN_PASSWORD
from helpers import (
    COURSE_ADD_URL, COURSE_LIST_URL,
    login_admin, body_text, assert_validation_error, admin_search,
    create_faculty_via_admin, create_course_via_admin,
    click_save, fill_if_exists, set_admin_autocomplete_value,
    set_checkbox_if_exists, unique,
)


def test_create_course_success(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    course = create_course_via_admin(driver)
    assert course["code"].lower() in body_text(driver).lower() or course["name"].lower() in body_text(driver).lower()


def test_create_course_empty_required_fields(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    driver.get(COURSE_ADD_URL)
    click_save(driver)
    assert_validation_error(driver)


def test_create_course_invalid_credit_sum(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    faculty = create_faculty_via_admin(driver)
    code = unique("BADCOURSE").upper().replace("_", "")[:18]

    driver.get(COURSE_ADD_URL)
    fill_if_exists(driver, "code", code)
    fill_if_exists(driver, "name", unique("Course_Invalid_Credit"))
    set_admin_autocomplete_value(driver, "faculty", faculty["id"], f"{faculty['code']} — {faculty['name']}")
    fill_if_exists(driver, "credits", "3.0")
    fill_if_exists(driver, "credits_lt", "1.0")
    fill_if_exists(driver, "credits_th", "1.0")
    set_checkbox_if_exists(driver, "is_active", True)
    click_save(driver)

    assert_validation_error(driver)


def test_create_course_duplicate_code(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    course = create_course_via_admin(driver)
    faculty = create_faculty_via_admin(driver)

    driver.get(COURSE_ADD_URL)
    fill_if_exists(driver, "code", course["code"])
    fill_if_exists(driver, "name", unique("Course_Duplicate"))
    set_admin_autocomplete_value(driver, "faculty", faculty["id"], f"{faculty['code']} — {faculty['name']}")
    fill_if_exists(driver, "credits", "3.0")
    fill_if_exists(driver, "credits_lt", "3.0")
    fill_if_exists(driver, "credits_th", "0.0")
    set_checkbox_if_exists(driver, "is_active", True)
    click_save(driver)

    assert_validation_error(driver)


def test_search_course_exists(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    course = create_course_via_admin(driver)
    text = admin_search(driver, COURSE_LIST_URL, course["code"])
    assert course["code"].lower() in text.lower()


def test_search_course_not_exists(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    text = admin_search(driver, COURSE_LIST_URL, "du_lieu_khong_ton_tai_999999")
    assert "0" in text or "không tìm thấy" in text.lower() or "0 results" in text.lower()
