# Bookstore Service

Project gồm 4 service Django (microservices):

- **api-gateway** – Cổng API
- **book-service** – Quản lý sách
- **cart-service** – Giỏ hàng
- **customer-service** – Khách hàng
- **comment-rate-service** – Đánh giá sách (rating + comment)

## Chạy project (dùng SQLite mặc định)

### 1. Cài đặt dependencies

```bash
cd bookstore-service
pip install -r requirements.txt
```

### 2. Chạy từng service (mỗi service một terminal, khác port)

**Terminal 1 – API Gateway (port 8000):**
```bash
cd api-gateway
python manage.py migrate
python manage.py runserver 8000
```

**Terminal 2 – Book Service (port 8001):**
```bash
cd book-service
python manage.py migrate
python manage.py runserver 8001
```

**Terminal 3 – Cart Service (port 8002):**
```bash
cd cart-service
python manage.py migrate
python manage.py runserver 8002
```

**Terminal 4 – Customer Service (port 8003):**
```bash
cd customer-service
python manage.py migrate
python manage.py runserver 8003
```

**Terminal 5 – Comment-Rate Service (port 8010):**
```bash
cd comment-rate-service
python manage.py migrate
python manage.py runserver 8010
```

Sau khi chạy:
- API Gateway: http://127.0.0.1:8000/
- Book Service: http://127.0.0.1:8001/
- Cart Service: http://127.0.0.1:8002/
- Customer Service: http://127.0.0.1:8003/
- Comment-Rate Service: http://127.0.0.1:8010/

---

## Chuyển sang MySQL

### 1. Cài MySQL và tạo database

Trong MySQL (hoặc MySQL Workbench), chạy:

```sql
CREATE DATABASE api_gateway_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE book_service_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE cart_service_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE customer_service_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Set biến môi trường rồi chạy từng service

Trên Linux/macOS (thay `your_password` bằng mật khẩu MySQL):

```bash
export DB_ENGINE=mysql
export DB_USER=root
export DB_PASSWORD=your_password
export DB_HOST=127.0.0.1
export DB_PORT=3306
```

Mỗi service dùng một database riêng (mặc định đã cấu hình trong code). Chạy từng service như bình thường:

```bash
# Terminal 1
cd api-gateway
export DB_NAME=api_gateway_db   # không bắt buộc, đã có mặc định
python manage.py migrate
python manage.py runserver 8000

# Terminal 2
cd book-service
export DB_NAME=book_service_db
python manage.py migrate
python manage.py runserver 8001

# Terminal 3
cd cart-service
export DB_NAME=cart_service_db
python manage.py migrate
python manage.py runserver 8002

# Terminal 4
cd customer-service
export DB_NAME=customer_service_db
python manage.py migrate
python manage.py runserver 8003
```

Trên Windows (CMD):

```cmd
set DB_ENGINE=mysql
set DB_USER=root
set DB_PASSWORD=your_password
set DB_HOST=127.0.0.1
set DB_PORT=3306
set DB_NAME=api_gateway_db
cd api-gateway
python manage.py migrate
python manage.py runserver 8000
```

(Làm tương tự cho từng service, đổi `DB_NAME` cho đúng.)

### 3. Biến môi trường MySQL (tùy chọn)

| Biến        | Mặc định              | Ý nghĩa                    |
|------------|------------------------|----------------------------|
| `DB_ENGINE`| (không set = SQLite)   | Set `mysql` để dùng MySQL  |
| `DB_NAME`  | Tên DB theo từng service | Tên database              |
| `DB_USER`  | `root`                 | User MySQL                 |
| `DB_PASSWORD` | ``                 | Mật khẩu MySQL             |
| `DB_HOST`  | `127.0.0.1`            | Host MySQL                 |
| `DB_PORT`  | `3306`                 | Port MySQL                 |

Nếu **không** set `DB_ENGINE=mysql`, project vẫn chạy bằng **SQLite** như cũ.

---

## Staff và Superuser

### Tạo nhân viên mẫu (Staff Service)
```bash
cd staff-service
python manage.py migrate
python manage.py create_sample_staff   # Tạo 3 nhân viên mẫu
```

### Tạo Superuser (admin/admin123)
```bash
# API Gateway (admin tại http://localhost:8000/admin/)
cd api-gateway
python manage.py create_superuser

# Staff Service (admin tại http://localhost:8004/admin/)
cd staff-service
python manage.py create_superuser
```

### Thêm nhân viên qua giao diện
- Vào **Thêm nhân viên** (menu) hoặc http://127.0.0.1:8000/staff/
- Điền form và nhấn "Thêm nhân viên"
