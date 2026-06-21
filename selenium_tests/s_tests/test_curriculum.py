from config import ADMIN_USERNAME, ADMIN_PASSWORD
from helpers import (
    CURRICULUM_ADD_URL, CURRICULUM_LIST_URL,
    login_admin, body_text, assert_validation_error, admin_search,
    create_curriculum_via_admin,
    click_save, click_save_js, fill_if_exists, set_hidden_select_value,
)


def test_create_curriculum_success(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    curriculum = create_curriculum_via_admin(driver)
    assert curriculum["id"] in driver.current_url or curriculum["major"]["code"].lower() in body_text(driver).lower()


def test_create_curriculum_empty_required_fields(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    driver.get(CURRICULUM_ADD_URL)
    click_save(driver)
    assert_validation_error(driver)


def test_create_curriculum_duplicate_major_year(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    curriculum = create_curriculum_via_admin(driver)
    major = curriculum["major"]
    year = curriculum["year"]

    driver.get(CURRICULUM_ADD_URL)

    # Trường major là Select2 autocomplete ẩn. Ở ca duplicate, Django Admin có JS
    # tự cập nhật field khoa nên DOM đôi khi bị stale. Set trực tiếp hidden select
    # và bấm lưu bằng JS để kiểm tra đúng nghiệp vụ unique_together(major, year).
    set_hidden_select_value(driver, "major", major["id"], major["name"])
    fill_if_exists(driver, "year", year)
    click_save_js(driver)

    assert_validation_error(driver)


def test_search_curriculum_exists(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    curriculum = create_curriculum_via_admin(driver)
    major = curriculum["major"]

    # CurriculumAdmin search_fields có major__code và major__name, nhưng list_display
    # hiển thị Major.__str__ = name, không hiển thị code. Vì vậy tìm bằng code
    # nhưng assert theo tên ngành/năm đang hiển thị trên bảng.
    text = admin_search(driver, CURRICULUM_LIST_URL, major["code"])
    lower = text.lower()
    assert major["name"].lower() in lower or curriculum["year"] in text


def test_search_curriculum_not_exists(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    text = admin_search(driver, CURRICULUM_LIST_URL, "du_lieu_khong_ton_tai_999999")
    assert "0" in text or "không tìm thấy" in text.lower() or "0 results" in text.lower()


def test_view_curriculum_list(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    driver.get(CURRICULUM_LIST_URL)
    text = body_text(driver).lower()
    assert "curriculum" in text or "chương trình" in text or "ctđt" in text or "curriculums" in text
