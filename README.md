# Bookstore Service – Microservices Architecture

Dự án mô phỏng **hệ thống nhà sách online** được xây dựng theo kiến trúc **Microservices** sử dụng **Django + Django REST Framework**.  
Mỗi chức năng được tách thành **service độc lập**, giao tiếp qua **HTTP REST API** và được điều phối bởi **API Gateway**.


# Technology Stack

- **Python 3**
- **Django**
- **Django REST Framework**
- **SQLite** (development database)
- **REST API**
- **Microservices Architecture**

---

# Services Overview

| Service | Description | Port |
|------|------|------|
| **api-gateway** | Entry point & routing requests | 8000 |
| **customer-service** | Customer management | 8001 |
| **cart-service** | Shopping cart management | 8002 |
| **book-service** | Books, Categories, Publishers | 8003 |
| **staff-service** | Staff management | 8004 |
| **manager-service** | Manager management | 8005 |
| **catalog-service** | Catalog aggregation | 8006 |
| **order-service** | Order processing | 8007 |
| **pay-service** | Payment processing | 8008 |
| **ship-service** | Shipping service | 8009 |
| **comment-rate-service** | Book reviews & ratings | 8010 |
| **recommender-ai-service** | AI book recommendation | 8011 |

---

# Quick Start

## 1. Clone Repository

```bash
git clone https://github.com/gxdumplingg/SOA---Assignment05---Bookstore-Service.git
cd bookstore-service
```

# Setup & Run Services

## 1. Install Dependencies

Di chuyển vào thư mục project và cài đặt các thư viện cần thiết:

```bash
cd /Users/lehuonggiang/Downloads/bookstore-service
pip install -r requirements.txt
```
## 2. Run All Services (SQLite)

Mỗi service cần chạy trong một terminal riêng.

### Terminal 1 – API Gateway (8000)
```bash
cd api-gateway
python3 manage.py migrate
python3 manage.py runserver 8000
```

### Terminal 2 – Customer Service (8001)
```bash
cd ../customer-service
python3 manage.py migrate
python3 manage.py runserver 8001
```

### Terminal 3 – Cart Service (8002)
```bash
cd ../cart-service
python3 manage.py migrate
python3 manage.py runserver 8002
```

### Terminal 4 – Book Service (8003)
```bash
cd ../book-service
python3 manage.py migrate
python3 manage.py runserver 8003
```

### Terminal 5 – Staff Service (8004)
```bash
cd ../staff-service
python3 manage.py migrate
python3 manage.py runserver 8004
```

### Terminal 6 – Manager Service (8005)
```bash
cd ../manager-service
python3 manage.py migrate
python3 manage.py runserver 8005
```

### Terminal 7 – Catalog Service (8006)
```bash
cd ../catalog-service
python3 manage.py migrate
python3 manage.py runserver 8006
```

### Terminal 8 – Order Service (8007)
```bash
cd ../order-service
python3 manage.py migrate
python3 manage.py runserver 8007
```

### Terminal 9 – Pay Service (8008)
```bash
cd ../pay-service
python3 manage.py migrate
python3 manage.py runserver 8008
```

### Terminal 10 – Ship Service (8009)
```bash
cd ../ship-service
python3 manage.py migrate
python3 manage.py runserver 8009
```

### Terminal 11 – Comment-Rate Service (8010)
```bash
cd ../comment-rate-service
python3 manage.py migrate
python3 manage.py runserver 8010
```

### Terminal 12 – Recommender AI Service (8011)
```bash
cd ../recommender-ai-service
python3 manage.py migrate
python3 manage.py runserver 8011
```

## 3. Access the Application
Sau khi tất cả services chạy thành công, truy cập:
```
http://127.0.0.1:8000/
```
Đây là API Gateway, nơi điều phối request đến các service backend khác.