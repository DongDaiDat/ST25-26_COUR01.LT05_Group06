# KIỂM THỬ VÀ ĐÁNH GIÁ CHẤT LƯỢNG HỆ THỐNG QUẢN LÝ ĐÀO TẠO UNIMIS

## 1. Giới thiệu

Đây là repository phục vụ đề tài môn học **Đánh giá và Kiểm định chất lượng phần mềm** với nội dung:

> **Kiểm thử và đánh giá chất lượng hệ thống Quản lý chương trình đào tạo UniMIS**

UniMIS là ứng dụng web hỗ trợ quản lý dữ liệu đào tạo trong môi trường đại học, bao gồm quản lý trường, khoa/viện, ngành đào tạo, học phần, chương trình đào tạo và danh sách học phần thuộc chương trình đào tạo.

Mục tiêu của nhóm là áp dụng kiểm thử tự động và kiểm thử chức năng để đánh giá tính đúng đắn của nghiệp vụ, tính ổn định của hệ thống và khả năng kiểm soát dữ liệu đầu vào.

---

## 2. Thành viên nhóm

| STT | Họ và tên        | Vai trò                                                                         |
| --: | ---------------- | ------------|
|   1 | Đồng Đại Đạt     | Trưởng nhóm |
|   2 | Nguyễn Cao Hải   | Thành viên  |
|   3 | Vương Xuân Giáp  | Thành viên  |
|   4 | Nguyễn Nam Khánh | Thành viên  |

---

## 3. Công nghệ và công cụ sử dụng

| Nhóm                       | Công nghệ / Công cụ    |
| -------------------------- | ---------------------- |
| Backend                    | Django, Python         |
| Cơ sở dữ liệu              | PostgreSQL             |
| Triển khai môi trường      | Docker, Docker Compose |
| Kiểm thử hộp trắng         | Django Test, Coverage  |
| Kiểm thử giao diện tự động | Selenium, pytest       |
| Kiểm thử API               | Postman                |
| Trình duyệt kiểm thử       | Google Chrome          |
| Quản lý mã nguồn           | GitHub                 |

---

## 4. Phạm vi kiểm thử

Nhóm thực hiện kiểm thử các chức năng chính của hệ thống UniMIS:

* Đăng nhập hệ thống.
* Quản lý trường và khoa/viện.
* Quản lý ngành đào tạo.
* Quản lý học phần.
* Quản lý chương trình đào tạo.
* Thêm học phần vào chương trình đào tạo.
* Tìm kiếm và lọc dữ liệu.
* Phân quyền người dùng.
* Xuất chương trình đào tạo dưới dạng PDF.
* Kiểm tra một số API tìm kiếm dữ liệu.

---

## 5. Các hoạt động đã thực hiện

### 5.1. Kiểm thử hộp trắng

Nhóm xây dựng kiểm thử đơn vị cho app `miscore`, tập trung vào các thành phần có logic nghiệp vụ chính:

* `models.py`: kiểm tra dữ liệu, ràng buộc nghiệp vụ, tính tổng tín chỉ và học phí.
* `views.py`: kiểm tra API, tìm kiếm, lọc dữ liệu và xử lý lỗi.
* `urls.py`: kiểm tra ánh xạ URL.
* `pdf_utils.py`: kiểm tra chức năng xuất PDF.
* `signals.py`: kiểm tra xử lý tự động khi thay đổi dữ liệu.

Kết quả coverage được ghi nhận trong báo cáo kiểm thử:

| Thành phần     | Coverage |
| -------------- | -------: |
| `models.py`    |      84% |
| `views.py`     |      72% |
| `pdf_utils.py` |      94% |
| `signals.py`   |     100% |
| `urls.py`      |     100% |
| `admin.py`     |      46% |
| **Tổng thể**   |  **79%** |

---

### 5.2. Kiểm thử hộp đen và Selenium

Nhóm xây dựng các kịch bản Selenium sử dụng pytest để kiểm tra hệ thống từ góc nhìn người dùng.

Các nội dung được kiểm tra gồm:

* Đăng nhập thành công và đăng nhập với dữ liệu không hợp lệ.
* Tạo trường, khoa, ngành, học phần và chương trình đào tạo.
* Kiểm tra dữ liệu bắt buộc.
* Kiểm tra dữ liệu trùng lặp.
* Kiểm tra số tín chỉ không hợp lệ.
* Tìm kiếm và lọc dữ liệu.
* Kiểm tra phân quyền truy cập.
* Thêm học phần vào chương trình đào tạo.
* Kiểm tra xuất PDF chương trình đào tạo.
* Kiểm tra một số API tìm kiếm.

---

### 5.3. Kiểm thử API bằng Postman

Nhóm đã chuẩn bị Postman Collection để kiểm tra các API của hệ thống.

Các API được đưa vào phạm vi kiểm thử gồm:

* API trường.
* API khoa.
* API ngành đào tạo.
* API học phần.
* API chương trình đào tạo.
* API danh sách học phần trong chương trình đào tạo.
* API thông tin người dùng hiện tại.
* API tìm kiếm và lọc dữ liệu.

Các tiêu chí kiểm tra API gồm:

* Mã phản hồi HTTP.
* Cấu trúc dữ liệu JSON trả về.
* Dữ liệu tìm kiếm và lọc.
* Phản hồi khi thiếu hoặc sai tham số.
* Kiểm tra quyền truy cập đối với API cần bảo vệ.

> Lưu ý: Kết quả Postman sẽ được cập nhật thêm sau khi chạy collection và lưu ảnh minh chứng request/response.

---

## 6. Kết quả kiểm thử tự động

Kết quả thực thi bộ kiểm thử Selenium/pytest:

| Chỉ số                        | Kết quả |
| ----------------------------- | ------: |
| Tổng số test case đã thực thi |      41 |
| Test case Pass                |      40 |
| Test case Fail                |       1 |
| Tỷ lệ Pass                    |  97,56% |

### Kết quả theo nhóm chức năng

| STT | Nhóm chức năng                          | File kiểm thử                      | Số test |   Pass |  Fail |
| --: | --------------------------------------- | ---------------------------------- | ------: | -----: | ----: |
|   1 | Quản lý học phần trong CTĐT và xuất PDF | `test_add_course_to_curriculum.py` |       4 |      4 |     0 |
|   2 | Quản lý học phần                        | `test_course.py`                   |       6 |      6 |     0 |
|   3 | Quản lý chương trình đào tạo            | `test_curriculum.py`               |       6 |      6 |     0 |
|   4 | Đăng nhập hệ thống                      | `test_login.py`                    |       4 |      4 |     0 |
|   5 | Quản lý ngành đào tạo                   | `test_major.py`                    |       5 |      5 |     0 |
|   6 | Phân quyền truy cập                     | `test_permission.py`               |       4 |      4 |     0 |
|   7 | Quản lý trường và khoa                  | `test_school.py`                   |       7 |      6 |     1 |
|   8 | Tìm kiếm, lọc dữ liệu và API tìm kiếm   | `test_search_filter.py`            |       5 |      5 |     0 |
|     | **Tổng cộng**                           |                                    |  **41** | **40** | **1** |

---

## 7. Lỗi đã ghi nhận

| Mã lỗi | Chức năng              | Test case                                   | Trạng thái       |
| ------ | ---------------------- | ------------------------------------------- | ---------------- |
| BUG-01 | Quản lý trường và khoa | `test_create_faculty_empty_required_fields` | Cần kiểm tra lại |

Test case trên kiểm tra việc tạo khoa khi người dùng chưa nhập đầy đủ trường bắt buộc. Kết quả test hiện đang Fail, cần chạy lại riêng test case này để xác định nguyên nhân cụ thể:

* Hệ thống cho phép lưu dữ liệu thiếu trường bắt buộc.
* Thông báo lỗi thực tế không đúng với nội dung mong đợi của test.
* Locator hoặc assertion trong Selenium chưa phù hợp với giao diện hiện tại.

---

## 8. Hướng dẫn chạy hệ thống

### Khởi động môi trường Docker

```bash
docker compose up -d --build
```

Sau khi hệ thống khởi động, truy cập:

```text
http://localhost:8000/
```

---

## 9. Hướng dẫn chạy kiểm thử hộp trắng

Chạy Django Test cho app `miscore`:

```bash
docker compose exec unimis_web python manage.py test miscore
```

Chạy kiểm tra coverage:

```bash
docker compose exec unimis_web coverage run manage.py test miscore
docker compose exec unimis_web coverage report
docker compose exec unimis_web coverage html
```

Báo cáo HTML coverage được tạo trong thư mục:

```text
htmlcov/
```

---

## 10. Hướng dẫn chạy kiểm thử Selenium

Di chuyển đến thư mục chứa Selenium test:

```bash
cd selenium_tests
```

Kích hoạt môi trường ảo trên Windows:

```bash
.venv\Scripts\activate
```

Chạy toàn bộ test:

```bash
pytest s_tests -v
```

Tạo báo cáo HTML:

```bash
pytest s_tests -v --html=report.html --self-contained-html
```

---

## 11. Hướng dẫn chạy kiểm thử Postman

1. Mở Postman.
2. Chọn **Import**.
3. Import file:

```text
UniMIS_Postman_Collection.json
```

4. Thiết lập biến môi trường:

```text
base_url = http://localhost:8000
```

5. Chạy từng request hoặc chạy toàn bộ collection.
6. Kiểm tra mã phản hồi HTTP, JSON response và kết quả test.

---

## 12. Hướng phát triển tiếp theo

Trong các giai đoạn tiếp theo, nhóm dự kiến mở rộng kiểm thử đối với:

* Chức năng sửa và xóa dữ liệu.
* Kiểm thử hiệu năng và tải đồng thời.
* Kiểm thử bảo mật nâng cao.
* Kiểm thử trên nhiều trình duyệt và thiết bị.
* Hoàn thiện toàn bộ Postman Collection và bổ sung kết quả thực thi API.
* Tăng coverage đối với `admin.py` và các nhánh xử lý chưa được bao phủ.

---

## 13. Kết luận

Kết quả kiểm thử cho thấy hệ thống UniMIS hoạt động tương đối ổn định trong phạm vi các chức năng đã kiểm tra. Bộ kiểm thử tự động thực hiện 41 test case, trong đó 40 test case đạt yêu cầu, tương ứng tỷ lệ Pass 97,56%.

Các chức năng quan trọng như đăng nhập, quản lý học phần, ngành đào tạo, chương trình đào tạo, thêm học phần vào chương trình đào tạo, tìm kiếm/lọc dữ liệu, phân quyền và xuất PDF đều đạt kết quả tốt trong phạm vi kiểm thử hiện tại.

Một test case liên quan đến kiểm tra trường bắt buộc khi tạo khoa cần được xác minh và kiểm thử lại. Đây là cơ sở để nhóm tiếp tục hoàn thiện hệ thống và nâng cao độ tin cậy của kết quả kiểm thử.
