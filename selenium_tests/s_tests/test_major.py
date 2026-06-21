from config import ADMIN_USERNAME, ADMIN_PASSWORD
from helpers import (
    MAJOR_ADD_URL, MAJOR_LIST_URL,
    login_admin, body_text, assert_validation_error, admin_search,
    create_faculty_via_admin, create_major_via_admin,
    click_save, fill_if_exists, set_admin_autocomplete_value,
    set_checkbox_if_exists, unique,
)


def test_create_major_success(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    major = create_major_via_admin(driver)
    assert major["code"].lower() in body_text(driver).lower() or major["name"].lower() in body_text(driver).lower()


def test_create_major_empty_required_fields(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    driver.get(MAJOR_ADD_URL)
    click_save(driver)
    assert_validation_error(driver)


def test_create_major_duplicate_code(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    major = create_major_via_admin(driver)
    faculty = create_faculty_via_admin(driver)

    driver.get(MAJOR_ADD_URL)
    set_admin_autocomplete_value(driver, "faculty", faculty["id"], f"{faculty['code']} — {faculty['name']}")
    fill_if_exists(driver, "code", major["code"])
    fill_if_exists(driver, "name", unique("Major_Duplicate"))
    set_checkbox_if_exists(driver, "is_active", True)
    click_save(driver)

    assert_validation_error(driver)


def test_search_major_exists(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    major = create_major_via_admin(driver)
    text = admin_search(driver, MAJOR_LIST_URL, major["code"])
    assert major["code"].lower() in text.lower()


def test_search_major_not_exists(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    text = admin_search(driver, MAJOR_LIST_URL, "du_lieu_khong_ton_tai_999999")
    assert "0" in text or "không tìm thấy" in text.lower() or "0 results" in text.lower()
