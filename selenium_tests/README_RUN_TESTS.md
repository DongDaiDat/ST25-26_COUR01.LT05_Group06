# Selenium tests cho UniMIS

Bộ test này được sửa lại để tránh lỗi `ElementNotInteractableException` trên Django Admin `autocomplete_fields`.

Nguyên nhân lỗi cũ: các trường `school`, `faculty`, `major` trong Django Admin là Select2 autocomplete nên thẻ `<select>` gốc bị ẩn. Nếu Selenium click/send_keys trực tiếp vào thẻ ẩn sẽ lỗi `element not interactable`.

Bản này xử lý bằng hàm `set_admin_autocomplete_value()` trong `helpers.py`: set giá trị vào select ẩn bằng JavaScript và trigger sự kiện `change`.

## Cách chạy

Đặt thư mục `selenium_tests` cùng cấp với `manage.py`, sau đó chạy app trước:

```bash
python manage.py runserver
```

Mở terminal khác:

```bash
cd selenium_tests
pytest s_tests -v
```

Xuất report:

```bash
pytest s_tests -v --html=reports/blackbox_selenium_report.html
```

Nếu tài khoản admin hoặc địa chỉ server khác, sửa trong `config.py`.
