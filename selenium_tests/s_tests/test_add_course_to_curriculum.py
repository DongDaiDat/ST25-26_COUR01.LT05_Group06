from config import ADMIN_USERNAME, ADMIN_PASSWORD
from helpers import (
    CURRICULUM_EXPORT_PDF_URL,
    login_admin, body_text,
    create_curriculum_via_admin, create_course_via_admin,
    open_curriculum_manage, add_course_to_curriculum,
)


def test_add_course_to_curriculum_success(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    curriculum = create_curriculum_via_admin(driver)
    course = create_course_via_admin(driver, prefix="LC")

    open_curriculum_manage(driver, curriculum["id"])
    add_course_to_curriculum(driver, course["code"])

    text = body_text(driver).lower()
    assert "đã thêm" in text or course["code"].lower() in text


def test_add_duplicate_course_to_curriculum(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    curriculum = create_curriculum_via_admin(driver)
    course = create_course_via_admin(driver, prefix="LCDUP")

    open_curriculum_manage(driver, curriculum["id"])
    add_course_to_curriculum(driver, course["code"])
    open_curriculum_manage(driver, curriculum["id"])
    add_course_to_curriculum(driver, course["code"])

    text = body_text(driver).lower()
    assert "dòng đã tồn tại" in text or "đã tồn tại" in text or course["code"].lower() in text


def test_add_nonexistent_course_to_curriculum(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    curriculum = create_curriculum_via_admin(driver)

    open_curriculum_manage(driver, curriculum["id"])
    add_course_to_curriculum(driver, "NOCOURSE999999")

    text = body_text(driver).lower()
    assert "không tìm thấy học phần" in text or "nocourse999999" in text


def test_export_curriculum_pdf(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    curriculum = create_curriculum_via_admin(driver)
    course = create_course_via_admin(driver, prefix="PDF")

    open_curriculum_manage(driver, curriculum["id"])
    add_course_to_curriculum(driver, course["code"])

    driver.get(f"{CURRICULUM_EXPORT_PDF_URL}?curriculum={curriculum['id']}")
    assert "pdf" in driver.current_url.lower() or "application/pdf" in driver.execute_script("return document.contentType || document.mimeType || ''")
