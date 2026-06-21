import re
import time

from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from config import BASE_URL, LOGIN_URL, ADMIN_USERNAME, ADMIN_PASSWORD, TEST_PREFIX


ADMIN_INDEX_URL = f"{BASE_URL}/admin/"
UNIVERSITY_ADD_URL = f"{BASE_URL}/admin/miscore/university/add/"
SCHOOL_LIST_URL = f"{BASE_URL}/admin/miscore/school/"
SCHOOL_ADD_URL = f"{BASE_URL}/admin/miscore/school/add/"
FACULTY_LIST_URL = f"{BASE_URL}/admin/miscore/faculty/"
FACULTY_ADD_URL = f"{BASE_URL}/admin/miscore/faculty/add/"
MAJOR_LIST_URL = f"{BASE_URL}/admin/miscore/major/"
MAJOR_ADD_URL = f"{BASE_URL}/admin/miscore/major/add/"
COURSE_LIST_URL = f"{BASE_URL}/admin/miscore/course/"
COURSE_ADD_URL = f"{BASE_URL}/admin/miscore/course/add/"
CURRICULUM_LIST_URL = f"{BASE_URL}/admin/miscore/curriculum/"
CURRICULUM_ADD_URL = f"{BASE_URL}/admin/miscore/curriculum/add/"
CURRICULUM_MANAGE_URL = f"{BASE_URL}/admin/miscore/curriculumformanage/all/"
CURRICULUM_EXPORT_PDF_URL = f"{BASE_URL}/admin/miscore/curriculumformanage/export-pdf/"
CURRICULUM_COPY_URL = f"{BASE_URL}/admin/miscore/curriculumcopytool/"


def unique(prefix: str) -> str:
    return f"{TEST_PREFIX}_{prefix}_{int(time.time() * 1000)}"


def wait_body(driver):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )


def body_text(driver) -> str:
    return wait_body(driver).text


def safe_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    try:
        WebDriverWait(driver, 5).until(lambda d: element.is_enabled())
        element.click()
    except ElementNotInteractableException:
        driver.execute_script("arguments[0].click();", element)


def safe_clear_and_type(driver, element, value: str):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    try:
        element.clear()
        element.send_keys(value)
    except ElementNotInteractableException:
        driver.execute_script(
            "arguments[0].value = arguments[1];"
            "arguments[0].dispatchEvent(new Event('input', {bubbles: true}));"
            "arguments[0].dispatchEvent(new Event('change', {bubbles: true}));",
            element,
            value,
        )


def page_has_success(driver, *keywords: str) -> bool:
    text = body_text(driver).lower()
    success_words = [
        "đã được thêm thành công",
        "was added successfully",
        "đã thêm",
        "đã lưu",
        "thành công",
        "successfully",
    ]
    return any(w in text for w in success_words) or any(k.lower() in text for k in keywords)


def assert_validation_error(driver):
    text = body_text(driver).lower()
    assert (
        "trường này là bắt buộc" in text
        or "please correct the errors below" in text
        or "this field is required" in text
        or "bắt buộc" in text
        or "không hợp lệ" in text
        or "lỗi" in text
        or "error" in text
        or "đã tồn tại" in text
        or "already exists" in text
    )


def login_admin(driver, username=ADMIN_USERNAME, password=ADMIN_PASSWORD):
    driver.get(LOGIN_URL)
    safe_clear_and_type(driver, driver.find_element(By.NAME, "username"), username)
    safe_clear_and_type(driver, driver.find_element(By.NAME, "password"), password)
    safe_click(driver, driver.find_element(By.CSS_SELECTOR, "input[type='submit']"))

    WebDriverWait(driver, 10).until(lambda d: "/admin/login/" not in d.current_url)


def click_save(driver):
    safe_click(driver, driver.find_element(By.NAME, "_save"))


def click_save_and_continue(driver):
    safe_click(driver, driver.find_element(By.NAME, "_continue"))


def click_save_js(driver):
    """Click nút Lưu bằng JavaScript với selector mới, tránh StaleElementReference ở Django Admin."""
    driver.execute_script("""
        const btn = document.querySelector('input[name="_save"]');
        if (!btn) { throw new Error('Không tìm thấy nút _save'); }
        btn.click();
    """)


def set_hidden_select_value(driver, field_name: str, object_id, label: str):
    """
    Set giá trị cho <select> autocomplete ẩn nhưng không trigger Select2 change.
    Dùng cho các ca kiểm thử submit form sau khi DOM Django Admin dễ bị stale.
    """
    selected = driver.execute_script("""
        const fieldName = arguments[0];
        const value = String(arguments[1]);
        const label = String(arguments[2]);
        const select = document.querySelector('[name="' + fieldName + '"]');
        if (!select) { throw new Error('Không tìm thấy field: ' + fieldName); }
        select.innerHTML = '';
        const option = new Option(label, value, true, true);
        select.appendChild(option);
        select.value = value;
        return select.value;
    """, field_name, object_id, label)
    assert str(selected) == str(object_id), f"Không set được {field_name}={object_id}"
    return True


def parse_admin_object_id_from_url(url: str):
    match = re.search(r"/(\d+)/change/?", url)
    return match.group(1) if match else None


def set_checkbox_if_exists(driver, field_name: str, checked=True):
    elements = driver.find_elements(By.NAME, field_name)
    if not elements:
        return False
    element = elements[0]
    if element.is_selected() != checked:
        safe_click(driver, element)
    return True


def fill_if_exists(driver, field_name: str, value: str):
    elements = driver.find_elements(By.NAME, field_name)
    if not elements:
        return False
    safe_clear_and_type(driver, elements[0], value)
    return True


def set_admin_autocomplete_value(driver, field_name: str, object_id, label: str):
    """
    Dùng cho autocomplete_fields của Django Admin.
    Source của UniMIS dùng Select2 cho school/faculty/major/curriculum nên thẻ <select>
    bị ẩn, click/send_keys trực tiếp dễ gây ElementNotInteractableException.
    Hàm này set giá trị vào select ẩn bằng JS rồi trigger change.
    """
    script = r"""
        const fieldName = arguments[0];
        const value = String(arguments[1]);
        const label = String(arguments[2]);
        const select = document.querySelector('[name="' + fieldName + '"]');
        if (!select) {
            throw new Error('Không tìm thấy field autocomplete: ' + fieldName);
        }
        let option = Array.from(select.options).find(o => o.value === value);
        if (!option) {
            option = new Option(label, value, true, true);
            select.appendChild(option);
        }
        option.selected = true;
        select.value = value;
        select.dispatchEvent(new Event('input', {bubbles: true}));
        select.dispatchEvent(new Event('change', {bubbles: true}));
        if (window.django && django.jQuery) {
            django.jQuery(select).trigger('change');
        }
        return select.value;
    """
    selected = driver.execute_script(script, field_name, object_id, label)
    assert str(selected) == str(object_id), f"Không set được {field_name}={object_id}"
    return True


# Giữ lại tên cũ để các test cũ không lỗi import.
def select_admin_autocomplete(driver, field_name: str, search_text: str):
    # Fallback dùng UI Select2. Ưu tiên không dùng trong test mới vì khó ổn định.
    select_el = driver.find_element(By.NAME, field_name)
    select_id = select_el.get_attribute("id")
    containers = driver.find_elements(By.CSS_SELECTOR, f"#select2-{select_id}-container")
    if not containers:
        select = Select(select_el)
        for option in select.options:
            if option.get_attribute("value"):
                option.click()
                return True
        return False

    safe_click(driver, containers[0])
    search = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input.select2-search__field"))
    )
    search.send_keys(search_text)

    def valid_results(d):
        results = d.find_elements(By.CSS_SELECTOR, ".select2-results__option")
        visible = []
        for result in results:
            text = result.text.strip().lower()
            if not result.is_displayed():
                continue
            if not text:
                continue
            if "searching" in text or "đang tìm" in text or "loading" in text:
                continue
            if "no results" in text or "không tìm thấy" in text:
                continue
            visible.append(result)
        return visible

    results = WebDriverWait(driver, 10).until(valid_results)
    safe_click(driver, results[0])
    WebDriverWait(driver, 10).until(
        lambda d: d.find_element(By.NAME, field_name).get_attribute("value") not in (None, "")
    )
    return True


def admin_search(driver, list_url: str, keyword: str):
    driver.get(list_url)
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "searchbar"))
    )
    safe_clear_and_type(driver, search_box, keyword)
    submit_buttons = driver.find_elements(By.CSS_SELECTOR, "#changelist-search input[type='submit'], input[type='submit']")
    assert submit_buttons, "Không tìm thấy nút submit tìm kiếm trong Django Admin."
    safe_click(driver, submit_buttons[0])
    return body_text(driver)


# =========================
# Data creation through Django Admin UI
# =========================
def create_school_via_admin(driver):
    name = unique("School")
    driver.get(SCHOOL_ADD_URL)
    fill_if_exists(driver, "name", name)
    set_checkbox_if_exists(driver, "is_active", True)
    click_save_and_continue(driver)

    WebDriverWait(driver, 10).until(lambda d: "/change/" in d.current_url)
    school_id = parse_admin_object_id_from_url(driver.current_url)
    assert school_id, f"Không lấy được id School từ URL: {driver.current_url}"
    assert page_has_success(driver, name)
    return {"id": school_id, "name": name}


def create_faculty_via_admin(driver):
    school = create_school_via_admin(driver)
    code = unique("FAC").upper().replace("_", "")[:45]
    name = unique("Faculty")

    driver.get(FACULTY_ADD_URL)
    set_admin_autocomplete_value(driver, "school", school["id"], school["name"])
    fill_if_exists(driver, "code", code)
    fill_if_exists(driver, "name", name)
    set_checkbox_if_exists(driver, "is_active", True)
    click_save_and_continue(driver)

    WebDriverWait(driver, 10).until(lambda d: "/change/" in d.current_url)
    faculty_id = parse_admin_object_id_from_url(driver.current_url)
    assert faculty_id, f"Không lấy được id Faculty từ URL: {driver.current_url}"
    assert page_has_success(driver, name, code)
    return {"id": faculty_id, "school": school, "code": code, "name": name}


def create_major_via_admin(driver):
    faculty = create_faculty_via_admin(driver)
    code = unique("MAJ").upper().replace("_", "")[:45]
    name = unique("Major")

    driver.get(MAJOR_ADD_URL)
    set_admin_autocomplete_value(driver, "faculty", faculty["id"], f"{faculty['code']} — {faculty['name']}")
    fill_if_exists(driver, "code", code)
    fill_if_exists(driver, "name", name)
    set_checkbox_if_exists(driver, "is_active", True)
    click_save_and_continue(driver)

    WebDriverWait(driver, 10).until(lambda d: "/change/" in d.current_url)
    major_id = parse_admin_object_id_from_url(driver.current_url)
    assert major_id, f"Không lấy được id Major từ URL: {driver.current_url}"
    assert page_has_success(driver, name, code)
    return {"id": major_id, "faculty": faculty, "code": code, "name": name}


def create_course_via_admin(driver, prefix="COURSE", credits="3.0", credits_lt="3.0", credits_th="0.0"):
    faculty = create_faculty_via_admin(driver)
    code = unique(prefix).upper().replace("_", "")[:18]
    name = unique("Course")

    driver.get(COURSE_ADD_URL)
    fill_if_exists(driver, "code", code)
    fill_if_exists(driver, "name", name)
    set_admin_autocomplete_value(driver, "faculty", faculty["id"], f"{faculty['code']} — {faculty['name']}")
    fill_if_exists(driver, "credits", credits)
    fill_if_exists(driver, "credits_lt", credits_lt)
    fill_if_exists(driver, "credits_th", credits_th)
    set_checkbox_if_exists(driver, "is_active", True)
    click_save_and_continue(driver)

    WebDriverWait(driver, 10).until(lambda d: "/change/" in d.current_url)
    course_id = parse_admin_object_id_from_url(driver.current_url)
    assert course_id, f"Không lấy được id Course từ URL: {driver.current_url}"
    assert page_has_success(driver, name, code)
    return {"id": course_id, "faculty": faculty, "code": code, "name": name}


def create_curriculum_via_admin(driver, year=None):
    major = create_major_via_admin(driver)
    if year is None:
        year = str(2026 + (int(time.time() * 1000) % 3000))

    driver.get(CURRICULUM_ADD_URL)
    set_admin_autocomplete_value(driver, "major", major["id"], f"{major['code']} — {major['name']}")
    fill_if_exists(driver, "year", str(year))
    click_save_and_continue(driver)

    WebDriverWait(driver, 10).until(lambda d: "/change/" in d.current_url)
    curriculum_id = parse_admin_object_id_from_url(driver.current_url)
    assert curriculum_id, f"Không lấy được id CTĐT từ URL: {driver.current_url}"
    assert page_has_success(driver, major["code"], str(year))
    return {"id": curriculum_id, "major": major, "year": str(year)}


def open_curriculum_manage(driver, curriculum_id):
    driver.get(f"{CURRICULUM_MANAGE_URL}?curriculum={curriculum_id}")
    wait_body(driver)


def add_course_to_curriculum(driver, course_code: str):
    course_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "new_course_code"))
    )
    safe_clear_and_type(driver, course_input, course_code)

    semester = driver.find_element(By.NAME, "new_semester_no")
    safe_clear_and_type(driver, semester, "1")

    Select(driver.find_element(By.NAME, "new_requirement_type")).select_by_value("COMPULSORY")

    category = driver.find_elements(By.NAME, "new_category")
    if category:
        safe_clear_and_type(driver, category[0], "Selenium")

    notes = driver.find_elements(By.NAME, "new_notes")
    if notes:
        safe_clear_and_type(driver, notes[0], "Thêm bằng Selenium")

    safe_click(driver, driver.find_element(By.NAME, "add_row"))
    wait_body(driver)
