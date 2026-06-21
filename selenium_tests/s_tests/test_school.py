from config import ADMIN_USERNAME, ADMIN_PASSWORD
from helpers import (
    SCHOOL_ADD_URL, SCHOOL_LIST_URL, FACULTY_ADD_URL, FACULTY_LIST_URL,
    login_admin, body_text, assert_validation_error, admin_search,
    create_school_via_admin, create_faculty_via_admin, click_save,
)


def test_create_school_success(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    school = create_school_via_admin(driver)
    assert school["name"].lower() in body_text(driver).lower()


def test_create_school_empty_name(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    driver.get(SCHOOL_ADD_URL)
    click_save(driver)
    assert_validation_error(driver)


def test_create_faculty_success(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    faculty = create_faculty_via_admin(driver)
    assert faculty["code"].lower() in body_text(driver).lower() or faculty["name"].lower() in body_text(driver).lower()


def test_create_faculty_empty_required_fields(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    driver.get(FACULTY_ADD_URL)
    click_save(driver)
    assert_validation_error(driver)


def test_search_school_exists(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    school = create_school_via_admin(driver)
    text = admin_search(driver, SCHOOL_LIST_URL, school["name"])
    assert school["name"].lower() in text.lower()


def test_search_faculty_exists(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    faculty = create_faculty_via_admin(driver)
    text = admin_search(driver, FACULTY_LIST_URL, faculty["code"])
    assert faculty["code"].lower() in text.lower()


def test_search_faculty_not_exists(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    text = admin_search(driver, FACULTY_LIST_URL, "du_lieu_khong_ton_tai_999999")
    assert "0" in text or "không tìm thấy" in text.lower() or "0 results" in text.lower()
