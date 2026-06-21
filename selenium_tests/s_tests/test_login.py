from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from config import LOGIN_URL, ADMIN_USERNAME, ADMIN_PASSWORD


def test_login_success(driver):
    driver.get(LOGIN_URL)
    driver.find_element(By.NAME, "username").send_keys(ADMIN_USERNAME)
    driver.find_element(By.NAME, "password").send_keys(ADMIN_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    WebDriverWait(driver, 10).until(lambda d: "/admin/login/" not in d.current_url)
    assert "/admin/login/" not in driver.current_url


def test_login_wrong_password(driver):
    driver.get(LOGIN_URL)
    driver.find_element(By.NAME, "username").send_keys(ADMIN_USERNAME)
    driver.find_element(By.NAME, "password").send_keys("sai_mat_khau")
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    WebDriverWait(driver, 10).until(lambda d: "/admin/login/" in d.current_url)
    assert "/admin/login/" in driver.current_url


def test_login_empty_username(driver):
    driver.get(LOGIN_URL)
    username_input = driver.find_element(By.NAME, "username")
    driver.find_element(By.NAME, "password").send_keys(ADMIN_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    assert username_input.get_attribute("validationMessage") != ""


def test_login_empty_password(driver):
    driver.get(LOGIN_URL)
    password_input = driver.find_element(By.NAME, "password")
    driver.find_element(By.NAME, "username").send_keys(ADMIN_USERNAME)
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    assert password_input.get_attribute("validationMessage") != ""
