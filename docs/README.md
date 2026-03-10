# API Documentation (OpenAPI / Swagger)

Thư mục này chứa tài liệu API dạng **OpenAPI 3.0** cho toàn bộ microservices của Bookstore.

## File

- **`openapi.yaml`** – Định nghĩa đầy đủ API (paths, methods, request/response schemas) cho tất cả các service.

## Cách dùng với Swagger

### 1. Swagger Editor (online)

1. Mở [https://editor.swagger.io](https://editor.swagger.io).
2. **File → Import file** (hoặc paste nội dung) chọn `openapi.yaml`.
3. Bên phải sẽ hiển thị tài liệu và có thể **Try it out** cho từng endpoint.

### 2. Swagger UI (local bằng Docker)

```bash
docker run -p 8080:8080 -e SWAGGER_JSON=/foo/openapi.yaml -v $(pwd)/openapi.yaml:/foo/openapi.yaml swaggerapi/swagger-ui
```

Sau đó mở `http://localhost:8080`. Trong Swagger UI, chọn **Servers** (dropdown phía trên) để đổi base URL sang đúng port của từng service (8001–8011).

### 3. Tích hợp vào Django (drf-spectacular)

Nếu muốn generate OpenAPI từ code Django REST Framework:

```bash
pip install drf-spectacular
```

Trong `settings.py` của từng service:

```python
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
SPECTACULAR_SETTINGS = {
    'TITLE': 'Bookstore API',
    'VERSION': '1.0.0',
}
```

Trong `urls.py`:

```python
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
```

File `openapi.yaml` trong thư mục này có thể dùng làm tài liệu tham chiếu chung cho toàn bộ hệ thống (đa service) thay vì chỉ một Django app.

## Lưu ý

- Mỗi **service** chạy trên một **port** riêng (8001–8011). Trong OpenAPI đã khai báo nhiều `servers`; khi gọi API cần chọn đúng server (port) cho từng nhóm endpoint (Customer, Cart, Book, …).
- **API Gateway** (port 8000) chủ yếu phục vụ giao diện web (HTML), không phải REST API; các API được gọi từ Gateway tới các service backend tương ứng.
