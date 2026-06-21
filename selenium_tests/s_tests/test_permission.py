from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from config import BASE_URL, LOGIN_URL, ADMIN_USERNAME, ADMIN_PASSWORD
from helpers import COURSE_ADD_URL, login_admin, body_text


def test_unauthenticated_user_redirected_to_login(driver):
    driver.get(COURSE_ADD_URL)
    WebDriverWait(driver, 10).until(lambda d: "/admin/login/" in d.current_url)
    assert "/admin/login/" in driver.current_url


def test_admin_can_access_course_create_page(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    driver.get(COURSE_ADD_URL)
    text = body_text(driver).lower()
    assert "thêm" in text or "add" in text or "course" in text


def test_wrong_password_cannot_access_admin(driver):
    driver.get(LOGIN_URL)
    driver.find_element(By.NAME, "username").send_keys(ADMIN_USERNAME)
    driver.find_element(By.NAME, "password").send_keys("sai_mat_khau")
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    WebDriverWait(driver, 10).until(lambda d: "/admin/login/" in d.current_url)
    assert "/admin/login/" in driver.current_url


def test_after_login_admin_home_contains_miscore(driver):
    login_admin(driver, ADMIN_USERNAME, ADMIN_PASSWORD)
    driver.get(f"{BASE_URL}/admin/")
    text = body_text(driver).lower()
    assert "miscore" in text and "courses" in text
