import os
import requests
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

CUSTOMER_SERVICE_URL = os.getenv("CUSTOMER_SERVICE_URL", "http://localhost:8001")
BOOK_SERVICE_URL = os.getenv("BOOK_SERVICE_URL", "http://localhost:8003")
CART_SERVICE_URL = os.getenv("CART_SERVICE_URL", "http://localhost:8002")
ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://localhost:8007")
PAY_SERVICE_URL = os.getenv("PAY_SERVICE_URL", "http://localhost:8008")
SHIP_SERVICE_URL = os.getenv("SHIP_SERVICE_URL", "http://localhost:8009")
STAFF_SERVICE_URL = os.getenv("STAFF_SERVICE_URL", "http://localhost:8004")
COMMENT_RATE_SERVICE_URL = os.getenv("COMMENT_RATE_SERVICE_URL", "http://localhost:8010")
RECOMMENDER_URL = os.getenv("RECOMMENDER_SERVICE_URL", "http://localhost:8011")



def home(request):
    """Homepage with links to all features"""
    return render(request, 'home.html')


@csrf_protect
def register_customer(request):
    """Display customer registration form and handle submission"""
    if request.method == 'POST':
        name = request.POST.get('name')
        full_name = request.POST.get('full_name') or name
        email = request.POST.get('email')
        line1 = request.POST.get('line1')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        
        if not name or not email:
            messages.error(request, 'Vui lòng điền đầy đủ Họ và tên, Email!')
            return render(request, 'register.html')
        
        try:
            # Call customer service API to create customer
            response = requests.post(
                f"{CUSTOMER_SERVICE_URL}/api/customers/",
                json={
                    "name": name,
                    "email": email,
                    "fullname": {"full_name": full_name},
                    "address": {
                        "line1": line1 or "",
                        "city": city or "",
                        "state": state or "",
                        "postal_code": postal_code or "",
                        "country": country or "",
                        "is_default": True,
                    },
                },
                timeout=5
            )
            
            if response.status_code == 201:
                customer_data = response.json()
                messages.success(request, f'Đăng ký thành công! Chào mừng {customer_data["name"]}!')
                return redirect('customer_list')
            else:
                error_msg = response.json().get('email', ['Email đã tồn tại hoặc không hợp lệ'])[0]
                messages.error(request, f'Lỗi: {error_msg}')
        except requests.RequestException as e:
            messages.error(request, f'Không thể kết nối đến Customer Service. Vui lòng thử lại!')
        
        return render(request, 'register.html')
    
    return render(request, 'register.html')


def customer_list(request):
    """Display list of all customers"""
    try:
        response = requests.get(
            f"{CUSTOMER_SERVICE_URL}/api/customers/",
            timeout=5
        )
        
        if response.status_code == 200:
            customers = response.json()
        else:
            customers = []
            messages.error(request, 'Không thể tải danh sách khách hàng')
    except requests.RequestException:
        customers = []
        messages.error(request, 'Không thể kết nối đến Customer Service')
    
    return render(request, 'customer_list.html', {'customers': customers})


def book_list(request):
    """Display list of all books"""
    try:
        response = requests.get(
            f"{BOOK_SERVICE_URL}/api/books/",
            timeout=5
        )
        if response.status_code == 200:
            books = response.json()
        else:
            books = []
            messages.error(request, 'Không thể tải danh sách sách')
    except requests.RequestException:
        books = []
        messages.error(request, 'Không thể kết nối đến Book Service')
    # Get customer_id from session or query param
    customer_id = request.session.get('customer_id') or request.GET.get('customer_id')
    # Lọc theo category / publisher
    category_filter = request.GET.get('category') or ''
    publisher_filter = request.GET.get('publisher') or ''
    categories = {}
    publishers = {}
    for b in books:
        cat = b.get('category')
        if cat and cat.get('id') is not None:
            categories[cat['id']] = cat.get('name') or str(cat['id'])
        pub = b.get('publisher')
        if pub and pub.get('id') is not None:
            publishers[pub['id']] = pub.get('name') or str(pub['id'])
    if category_filter or publisher_filter:
        filtered = []
        for b in books:
            keep = True
            if category_filter:
                bid_cat = (b.get('category') or {}).get('id')
                if str(bid_cat) != category_filter:
                    keep = False
            if keep and publisher_filter:
                bid_pub = (b.get('publisher') or {}).get('id')
                if str(bid_pub) != publisher_filter:
                    keep = False
            if keep:
                filtered.append(b)
        books = filtered

    # Phân trang
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1
    per_page = 8
    total_books = len(books)
    num_pages = max((total_books + per_page - 1) // per_page, 1)
    if page < 1:
        page = 1
    if page > num_pages:
        page = num_pages
    start = (page - 1) * per_page
    end = start + per_page
    books_page = books[start:end]

    # Lấy đánh giá của chính khách này
    my_ratings_by_book = {}
    if customer_id:
        try:
            r = requests.get(
                f"{COMMENT_RATE_SERVICE_URL}/api/ratings/customer/{customer_id}/",
                timeout=5
            )
            if r.status_code == 200:
                for rr in r.json():
                    bid = rr.get('book_id')
                    if bid is not None:
                        my_ratings_by_book[int(bid)] = rr
        except requests.RequestException:
            pass
    for b in books_page:
        try:
            b['my_rating'] = my_ratings_by_book.get(int(b.get('id')))
        except Exception:
            b['my_rating'] = None
    # Gọi recommender-ai-service
    recommendations = []
    try:
        rec_resp = requests.get(f"{RECOMMENDER_URL}/api/recommendations/?limit=5", timeout=5)
        if rec_resp.status_code == 200:
            recommendations = rec_resp.json()
    except requests.RequestException:
        pass
    return render(request, 'book_list.html', {
        'books': books_page,
        'customer_id': customer_id,
        'categories': [{'id': cid, 'name': categories[cid]} for cid in sorted(categories.keys())],
        'publishers': [{'id': pid, 'name': publishers[pid]} for pid in sorted(publishers.keys())],
        'category_filter': category_filter,
        'publisher_filter': publisher_filter,
        'page': page,
        'num_pages': num_pages,
        'total_books': total_books,
        'recommendations': recommendations,
    })



@csrf_protect
def add_to_cart(request):
    """Add book to cart"""
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        book_id = request.POST.get('book_id')
        quantity = request.POST.get('quantity', 1)
        
        if not customer_id:
            messages.error(request, 'Vui lòng chọn khách hàng trước!')
            return redirect('book_list')
        
        try:
            # Get or create cart for customer
            cart_response = requests.get(
                f"{CART_SERVICE_URL}/api/carts/customer/{customer_id}/",
                timeout=5
            )
            
            if cart_response.status_code == 404:
                # Create new cart
                create_cart_response = requests.post(
                    f"{CART_SERVICE_URL}/api/carts/",
                    json={"customer_id": int(customer_id)},
                    timeout=5
                )
                if create_cart_response.status_code == 201:
                    cart_data = create_cart_response.json()
                    cart_id = cart_data['id']
                else:
                    messages.error(request, 'Không thể tạo giỏ hàng!')
                    return redirect('book_list')
            elif cart_response.status_code == 200:
                cart_data = cart_response.json()
                cart_id = cart_data['id']
            else:
                messages.error(request, 'Không thể lấy thông tin giỏ hàng!')
                return redirect('book_list')
            
            # Add item to cart
            add_response = requests.post(
                f"{CART_SERVICE_URL}/api/carts/{cart_id}/add-item/",
                json={"book_id": int(book_id), "quantity": int(quantity)},
                timeout=5
            )
            
            if add_response.status_code == 200:
                messages.success(request, 'Đã thêm sách vào giỏ hàng!')
                # Store customer_id in session
                request.session['customer_id'] = customer_id
                return redirect('view_cart')
            else:
                messages.error(request, 'Không thể thêm sách vào giỏ hàng!')
        except requests.RequestException:
            messages.error(request, 'Không thể kết nối đến Cart Service!')
        
        return redirect('book_list')
    
    return redirect('book_list')


def view_cart(request):
    """View cart contents"""
    customer_id = request.session.get('customer_id') or request.GET.get('customer_id')
    
    if not customer_id:
        messages.error(request, 'Vui lòng chọn khách hàng!')
        return redirect('customer_list')
    
    cart_items = []
    total_price = 0
    customer = None
    cart_id = None
    
    try:
        # Get customer info
        customer_response = requests.get(
            f"{CUSTOMER_SERVICE_URL}/api/customers/{customer_id}/",
            timeout=5
        )
        if customer_response.status_code == 200:
            customer = customer_response.json()
        
        # Get cart
        cart_response = requests.get(
            f"{CART_SERVICE_URL}/api/carts/customer/{customer_id}/",
            timeout=5
        )
        
        if cart_response.status_code == 200:
            cart_data = cart_response.json()
            cart_id = cart_data['id']
            
            # Get book details for each cart item
            for item in cart_data.get('items', []):
                book_response = requests.get(
                    f"{BOOK_SERVICE_URL}/api/books/{item['book_id']}/",
                    timeout=5
                )
                if book_response.status_code == 200:
                    book = book_response.json()
                    item_total = float(book['price']) * item['quantity']
                    cart_items.append({
                        'id': item['id'],
                        'book': book,
                        'quantity': item['quantity'],
                        'total': item_total
                    })
                    total_price += item_total
        elif cart_response.status_code == 404:
            messages.info(request, 'Giỏ hàng trống!')
    except requests.RequestException:
        messages.error(request, 'Không thể tải giỏ hàng!')
    
    request.session['customer_id'] = customer_id
    
    return render(request, 'cart.html', {
        'customer': customer,
        'customer_id': customer_id,
        'cart_id': cart_id,
        'cart_items': cart_items,
        'total_price': total_price
    })


@csrf_protect
def checkout(request):
    """Trang thanh toán: GET hiển thị form chọn phương thức, POST tạo order + payment."""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        messages.error(request, 'Vui lòng chọn khách hàng trước khi thanh toán!')
        return redirect('customer_list')

    # GET: hiển thị trang thanh toán (giỏ hàng + form chọn phương thức)
    if request.method == 'GET':
        cart_items = []
        total_price = 0
        customer = None
        try:
            customer_response = requests.get(
                f"{CUSTOMER_SERVICE_URL}/api/customers/{customer_id}/",
                timeout=5
            )
            if customer_response.status_code == 200:
                customer = customer_response.json()

            cart_response = requests.get(
                f"{CART_SERVICE_URL}/api/carts/customer/{customer_id}/",
                timeout=5
            )
            if cart_response.status_code == 200:
                cart_data = cart_response.json()
                for item in cart_data.get('items', []):
                    book_resp = requests.get(
                        f"{BOOK_SERVICE_URL}/api/books/{item['book_id']}/",
                        timeout=5
                    )
                    if book_resp.status_code == 200:
                        book = book_resp.json()
                        item_total = float(book['price']) * item['quantity']
                        cart_items.append({
                            'id': item['id'],
                            'book': book,
                            'quantity': item['quantity'],
                            'total': item_total
                        })
                        total_price += item_total
        except requests.RequestException:
            messages.error(request, 'Không thể tải thông tin giỏ hàng.')
            return redirect('view_cart')

        if not cart_items:
            messages.error(request, 'Giỏ hàng trống, không thể thanh toán.')
            return redirect('view_cart')

        return render(request, 'checkout.html', {
            'customer': customer,
            'customer_id': customer_id,
            'cart_items': cart_items,
            'total_price': total_price
        })

    # POST: xác nhận thanh toán → tạo order + payment + shipment
    payment_method = request.POST.get('payment_method', 'CASH')
    if payment_method not in ('CASH', 'CARD', 'BANK'):
        payment_method = 'CASH'
    shipping_method = request.POST.get('shipping_method', 'STANDARD')
    if shipping_method not in ('STANDARD', 'EXPRESS', 'PICKUP'):
        shipping_method = 'STANDARD'

    try:
        cart_response = requests.get(
            f"{CART_SERVICE_URL}/api/carts/customer/{customer_id}/",
            timeout=5
        )
        if cart_response.status_code != 200:
            messages.error(request, 'Không thể lấy giỏ hàng để tạo đơn hàng!')
            return redirect('view_cart')

        cart_data = cart_response.json()
        items_payload = []
        total_price = 0

        for item in cart_data.get('items', []):
            book_resp = requests.get(
                f"{BOOK_SERVICE_URL}/api/books/{item['book_id']}/",
                timeout=5
            )
            if book_resp.status_code == 200:
                book = book_resp.json()
                price = float(book.get('price', 0))
                qty = item['quantity']
                items_payload.append({
                    "book_id": item["book_id"],
                    "quantity": qty,
                    "price": price,
                })
                total_price += price * qty

        if not items_payload:
            messages.error(request, 'Giỏ hàng trống, không thể tạo đơn hàng!')
            return redirect('view_cart')

        # 1. Tạo đơn hàng (order-service)
        order_resp = requests.post(
            f"{ORDER_SERVICE_URL}/api/orders/",
            json={
                "customer_id": int(customer_id),
                "items": items_payload,
            },
            timeout=5,
        )

        if order_resp.status_code not in (200, 201):
            messages.error(request, 'Không thể tạo đơn hàng!')
            return redirect('view_cart')

        order = order_resp.json()
        order_id = order.get('id')

        # 2. Tạo payment (pay-service)
        pay_resp = requests.post(
            f"{PAY_SERVICE_URL}/api/payments/",
            json={
                "order_id": order_id,
                "amount": str(total_price),
                "method": payment_method,
                "status": "COMPLETED",
            },
            timeout=5,
        )

        if pay_resp.status_code in (200, 201):
            pay_data = pay_resp.json()
            pay_msg = f"Thanh toán thành công (Mã #{pay_data.get('id')})"
        else:
            pay_msg = "Đơn hàng đã tạo. Lưu ý: Pay Service chưa ghi nhận thanh toán."

        # 3. Tạo shipment (ship-service)
        ship_resp = requests.post(
            f"{SHIP_SERVICE_URL}/api/shipments/",
            json={
                "order_id": order_id,
                "method": shipping_method,
                "status": "PENDING",
            },
            timeout=5,
        )
        if ship_resp.status_code in (200, 201):
            ship_data = ship_resp.json()
            ship_msg = f"Đơn vận chuyển #{ship_data.get('id')} ({shipping_method}) đã tạo."
        else:
            ship_msg = "Lưu ý: Ship Service chưa tạo đơn vận chuyển."

        messages.success(request, f"{pay_msg} Đơn hàng #{order_id}. {ship_msg}")

        # 4. Cập nhật order sang PAID
        try:
            requests.patch(
                f"{ORDER_SERVICE_URL}/api/orders/{order_id}/",
                json={"status": "PAID"},
                timeout=5
            )
        except requests.RequestException:
            pass

        # 5. Xóa giỏ hàng sau khi thanh toán thành công
        cart_id = cart_data.get('id')
        if cart_id:
            try:
                requests.delete(
                    f"{CART_SERVICE_URL}/api/carts/{cart_id}/clear/",
                    timeout=5
                )
            except requests.RequestException:
                pass

    except requests.RequestException:
        messages.error(request, 'Không thể kết nối đến Order, Pay hoặc Ship Service. Vui lòng thử lại!')

    return redirect('order_list')


def order_list(request):
    """Danh sách đơn hàng của khách hàng đang chọn (từ session)."""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        messages.info(request, 'Vui lòng chọn khách hàng để xem đơn hàng.')
        return redirect(f"{reverse('select_customer')}?next={reverse('order_list')}")

    orders = []
    try:
        resp = requests.get(f"{ORDER_SERVICE_URL}/api/orders/", timeout=5)
        if resp.status_code == 200:
            all_orders = resp.json()
            # Chỉ lấy đơn của khách đang chọn
            orders = [o for o in all_orders if o.get('customer_id') == int(customer_id)]
        else:
            messages.error(request, 'Không thể tải danh sách đơn hàng.')
    except requests.RequestException:
        messages.error(request, 'Không thể kết nối đến Order Service.')

    # Lấy tên khách hàng
    customer_name = f"KH#{customer_id}"
    try:
        cust_resp = requests.get(f"{CUSTOMER_SERVICE_URL}/api/customers/{customer_id}/", timeout=5)
        if cust_resp.status_code == 200:
            customer_name = cust_resp.json().get('name', customer_name)
    except requests.RequestException:
        pass

    # Tính tổng tiền, số lượng, format ngày mỗi đơn
    for order in orders:
        total = 0
        total_qty = 0
        for item in order.get('items', []):
            qty = int(item.get('quantity', 0))
            total += float(item.get('price', 0)) * qty
            total_qty += qty
        order['total_amount'] = total
        order['total_quantity'] = total_qty
        created_at = order.get('created_at')
        if created_at:
            try:
                dt = datetime.fromisoformat(str(created_at).replace('Z', '+00:00'))
                order['created_at_formatted'] = dt.strftime('%d/%m/%Y %H:%M')
            except (ValueError, TypeError):
                order['created_at_formatted'] = str(created_at)
        else:
            order['created_at_formatted'] = ''

    return render(request, 'order_list.html', {
        'orders': orders,
        'customer_name': customer_name,
    })


def order_detail(request, order_id):
    """Chi tiết đơn hàng - chỉ xem được đơn của khách đang chọn."""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        messages.info(request, 'Vui lòng chọn khách hàng để xem đơn hàng.')
        return redirect(f"{reverse('select_customer')}?next={reverse('order_list')}")

    try:
        resp = requests.get(f"{ORDER_SERVICE_URL}/api/orders/{order_id}/", timeout=5)
        if resp.status_code != 200:
            messages.error(request, 'Không tìm thấy đơn hàng.')
            return redirect('order_list')
        order = resp.json()
        if order.get('customer_id') != int(customer_id):
            messages.error(request, 'Bạn không có quyền xem đơn hàng này.')
            return redirect('order_list')
    except requests.RequestException:
        messages.error(request, 'Không thể kết nối đến Order Service.')
        return redirect('order_list')

    # Lấy tên sách cho từng item
    items_with_book = []
    total_amount = 0
    for item in order.get('items', []):
        book_title = f"Sách #{item.get('book_id')}"
        try:
            br = requests.get(f"{BOOK_SERVICE_URL}/api/books/{item.get('book_id')}/", timeout=5)
            if br.status_code == 200:
                book_title = br.json().get('title', book_title)
        except requests.RequestException:
            pass
        item_total = float(item.get('price', 0)) * int(item.get('quantity', 0))
        total_amount += item_total
        items_with_book.append({
            **item,
            'book_title': book_title,
            'item_total': item_total,
        })

    created_at = order.get('created_at')
    if created_at:
        try:
            dt = datetime.fromisoformat(str(created_at).replace('Z', '+00:00'))
            created_at_formatted = dt.strftime('%d/%m/%Y %H:%M')
        except (ValueError, TypeError):
            created_at_formatted = str(created_at)
    else:
        created_at_formatted = ''

    customer_name = f"KH#{customer_id}"
    try:
        cust_resp = requests.get(f"{CUSTOMER_SERVICE_URL}/api/customers/{customer_id}/", timeout=5)
        if cust_resp.status_code == 200:
            customer_name = cust_resp.json().get('name', customer_name)
    except requests.RequestException:
        pass

    # Lấy thông tin vận chuyển (ship-service)
    shipment = None
    SHIP_METHOD_LABELS = {"STANDARD": "Giao hàng tiêu chuẩn", "EXPRESS": "Giao hàng nhanh", "PICKUP": "Nhận tại cửa hàng"}
    SHIP_STATUS_LABELS = {"PENDING": "Chờ xử lý", "SHIPPED": "Đã giao", "DELIVERED": "Đã nhận", "CANCELLED": "Đã hủy"}
    try:
        ship_resp = requests.get(f"{SHIP_SERVICE_URL}/api/shipments/", timeout=5)
        if ship_resp.status_code == 200:
            all_shipments = ship_resp.json()
            for s in all_shipments:
                if s.get('order_id') == order_id:
                    shipment = s
                    shipment['method_label'] = SHIP_METHOD_LABELS.get(s.get('method'), s.get('method'))
                    shipment['status_label'] = SHIP_STATUS_LABELS.get(s.get('status'), s.get('status'))
                    break
            if shipment and shipment.get('created_at'):
                try:
                    dt = datetime.fromisoformat(str(shipment['created_at']).replace('Z', '+00:00'))
                    shipment['created_at_formatted'] = dt.strftime('%d/%m/%Y %H:%M')
                except (ValueError, TypeError):
                    shipment['created_at_formatted'] = str(shipment.get('created_at', ''))
            elif shipment:
                shipment['created_at_formatted'] = ''
    except requests.RequestException:
        pass

    return render(request, 'order_detail.html', {
        'order': order,
        'items': items_with_book,
        'total_amount': total_amount,
        'created_at_formatted': created_at_formatted,
        'customer_name': customer_name,
        'shipment': shipment,
    })


@csrf_protect
def remove_from_cart(request, cart_id, item_id):
    """Remove item from cart"""
    if request.method == 'POST':
        try:
            response = requests.delete(
                f"{CART_SERVICE_URL}/api/carts/{cart_id}/remove-item/{item_id}/",
                timeout=5
            )
            
            if response.status_code == 200:
                messages.success(request, 'Đã xóa sách khỏi giỏ hàng!')
            else:
                messages.error(request, 'Không thể xóa sách khỏi giỏ hàng!')
        except requests.RequestException:
            messages.error(request, 'Không thể kết nối đến Cart Service!')
    
    return redirect('view_cart')


@csrf_protect
def update_cart_item(request, cart_id, item_id):
    """Cập nhật số lượng mặt hàng trong giỏ."""
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity is not None:
            try:
                qty = int(quantity)
                if qty < 1:
                    qty = 1
                response = requests.put(
                    f"{CART_SERVICE_URL}/api/carts/{cart_id}/update-item/{item_id}/",
                    json={"quantity": qty},
                    timeout=5
                )
                if response.status_code == 200:
                    messages.success(request, 'Đã cập nhật số lượng!')
                else:
                    messages.error(request, 'Không thể cập nhật số lượng.')
            except (ValueError, requests.RequestException):
                messages.error(request, 'Có lỗi xảy ra khi cập nhật.')
    return redirect('view_cart')


def select_customer(request):
    """Chọn khách hàng và chuyển về trang next (mặc định: mua sắm)."""
    next_url = request.GET.get('next') or reverse('book_list')
    next_is_orders = next_url.startswith(reverse('order_list')) or next_url.startswith('/orders')

    try:
        response = requests.get(
            f"{CUSTOMER_SERVICE_URL}/api/customers/",
            timeout=5
        )
        
        if response.status_code == 200:
            customers = response.json()
        else:
            customers = []
            messages.error(request, 'Không thể tải danh sách khách hàng')
    except requests.RequestException:
        customers = []
        messages.error(request, 'Không thể kết nối đến Customer Service')
    
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        if customer_id:
            request.session['customer_id'] = customer_id

            next_post = request.POST.get('next') or reverse('book_list')
            if next_post in ('book_list', 'order_list'):
                return redirect(next_post)
            if url_has_allowed_host_and_scheme(next_post, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
                return redirect(next_post)
            return redirect('book_list')
    
    return render(request, 'select_customer.html', {
        'customers': customers,
        'next_url': next_url,
        'next_is_orders': next_is_orders,
    })


@csrf_protect
def rate_book(request, book_id):
    """Khách hàng đánh giá (1-5 sao) + bình luận cho sách."""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        messages.info(request, 'Vui lòng chọn khách hàng trước khi đánh giá.')
        return redirect('select_customer')

    book = None
    try:
        br = requests.get(f"{BOOK_SERVICE_URL}/api/books/{book_id}/", timeout=5)
        if br.status_code == 200:
            book = br.json()
    except requests.RequestException:
        pass
    if not book:
        messages.error(request, 'Không tìm thấy sách.')
        return redirect('book_list')

    existing = None
    try:
        r = requests.get(
            f"{COMMENT_RATE_SERVICE_URL}/api/ratings/customer/{customer_id}/",
            timeout=5
        )
        if r.status_code == 200:
            for rr in r.json():
                if rr.get('book_id') == int(book_id):
                    existing = rr
                    break
    except requests.RequestException:
        pass

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        try:
            rating_int = int(rating)
        except (TypeError, ValueError):
            rating_int = 0
        if rating_int < 1 or rating_int > 5:
            messages.error(request, 'Vui lòng chọn số sao từ 1 đến 5.')
            return render(request, 'rate_book.html', {'book': book, 'existing': existing})

        try:
            up = requests.post(
                f"{COMMENT_RATE_SERVICE_URL}/api/ratings/",
                json={
                    'customer_id': int(customer_id),
                    'book_id': int(book_id),
                    'rating': rating_int,
                    'comment': comment,
                },
                timeout=5
            )
            if up.status_code in (200, 201):
                messages.success(request, 'Đã lưu đánh giá của bạn!')
                return redirect('book_list')
            try:
                err = up.json()
                msg = err.get('detail') or err
            except ValueError:
                msg = up.text or f"Lỗi (HTTP {up.status_code})."
            messages.error(request, msg)
        except requests.RequestException:
            messages.error(request, 'Không thể kết nối đến Comment-Rate Service.')

    return render(request, 'rate_book.html', {'book': book, 'existing': existing})


# --- Staff manages books ---

@csrf_protect
def staff_register(request):
    """Thêm nhân viên mới (gọi Staff Service)."""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        role = request.POST.get('role', 'Nhân viên')
        department = request.POST.get('department', '')
        if name and email:
            try:
                r = requests.post(
                    f"{STAFF_SERVICE_URL}/api/staff/",
                    json={
                        'name': name,
                        'email': email,
                        'role': role,
                        'department': department,
                        'is_active': True,
                    },
                    timeout=5
                )
                if r.status_code in (200, 201):
                    messages.success(request, f'Đã thêm nhân viên {name}!')
                    return redirect('staff_book_list')
                err = r.json()
                msg = err.get('email', [err.get('detail', 'Lỗi')])
                if isinstance(msg, list):
                    msg = msg[0] if msg else 'Lỗi'
                messages.error(request, msg)
            except requests.RequestException:
                messages.error(request, 'Không thể kết nối đến Staff Service.')
        else:
            messages.error(request, 'Vui lòng điền tên và email.')
    return render(request, 'staff_register.html')


def staff_book_list(request):
    """Staff: danh sách sách, thêm/sửa/xóa."""
    staff_id = request.session.get('staff_id')
    staff = None
    staffs = []
    try:
        resp = requests.get(f"{STAFF_SERVICE_URL}/api/staff/", timeout=5)
        if resp.status_code == 200:
            staffs = resp.json()
        if staff_id:
            for s in staffs:
                if s.get('id') == int(staff_id):
                    staff = s
                    break
    except requests.RequestException:
        messages.error(request, 'Không thể kết nối đến Staff Service.')

    if request.method == 'POST' and request.POST.get('staff_id'):
        request.session['staff_id'] = request.POST.get('staff_id')
        return redirect('staff_book_list')

    books = []
    categories = []
    publishers = []
    try:
        r = requests.get(f"{BOOK_SERVICE_URL}/api/books/", timeout=5)
        if r.status_code == 200:
            books = r.json()
        cr = requests.get(f"{BOOK_SERVICE_URL}/api/categories/", timeout=5)
        if cr.status_code == 200:
            categories = cr.json()
        pr = requests.get(f"{BOOK_SERVICE_URL}/api/publishers/", timeout=5)
        if pr.status_code == 200:
            publishers = pr.json()
    except requests.RequestException:
        messages.error(request, 'Không thể tải danh sách sách hoặc danh mục.')

    return render(request, 'staff_book_list.html', {
        'books': books,
        'staffs': staffs,
        'staff': staff,
        'categories': categories,
        'publishers': publishers,
    })


@csrf_protect
def staff_book_add(request):
    """Staff: thêm sách mới."""
    staff_id = request.session.get('staff_id')
    if not staff_id:
        messages.info(request, 'Vui lòng chọn nhân viên trước khi quản lý sách.')
        return redirect('staff_book_list')

    categories = []
    publishers = []
    try:
        cr = requests.get(f"{BOOK_SERVICE_URL}/api/categories/", timeout=5)
        if cr.status_code == 200:
            categories = cr.json()
        pr = requests.get(f"{BOOK_SERVICE_URL}/api/publishers/", timeout=5)
        if pr.status_code == 200:
            publishers = pr.json()
    except requests.RequestException:
        messages.error(request, 'Không thể tải danh sách thể loại / nhà xuất bản.')

    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        description = request.POST.get('description', '')
        stock = request.POST.get('stock', 0)
        category_id = request.POST.get('category_id') or None
        publisher_id = request.POST.get('publisher_id') or None
        if title and author and price:
            try:
                payload = {
                    'title': title,
                    'author': author,
                    'price': float(price),
                    'description': description,
                    'stock': int(stock or 0),
                }
                if category_id:
                    payload['category_id'] = int(category_id)
                if publisher_id:
                    payload['publisher_id'] = int(publisher_id)

                r = requests.post(
                    f"{BOOK_SERVICE_URL}/api/books/",
                    json=payload,
                    timeout=5
                )
                if r.status_code in (200, 201):
                    messages.success(request, 'Đã thêm sách thành công!')
                    return redirect('staff_book_list')
                messages.error(request, r.json().get('detail', 'Lỗi khi thêm sách.'))
            except requests.RequestException:
                messages.error(request, 'Không thể kết nối đến Book Service.')
        else:
            messages.error(request, 'Vui lòng điền đầy đủ thông tin.')
    return render(request, 'staff_book_form.html', {
        'book': {},
        'action': 'add',
        'categories': categories,
        'publishers': publishers,
    })


@csrf_protect
def staff_book_edit(request, book_id):
    """Staff: sửa sách."""
    staff_id = request.session.get('staff_id')
    if not staff_id:
        messages.info(request, 'Vui lòng chọn nhân viên trước khi quản lý sách.')
        return redirect('staff_book_list')

    categories = []
    publishers = []
    try:
        cr = requests.get(f"{BOOK_SERVICE_URL}/api/categories/", timeout=5)
        if cr.status_code == 200:
            categories = cr.json()
        pr = requests.get(f"{BOOK_SERVICE_URL}/api/publishers/", timeout=5)
        if pr.status_code == 200:
            publishers = pr.json()
    except requests.RequestException:
        messages.error(request, 'Không thể tải danh sách thể loại / nhà xuất bản.')

    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        description = request.POST.get('description', '')
        stock = request.POST.get('stock', 0)
        category_id = request.POST.get('category_id') or None
        publisher_id = request.POST.get('publisher_id') or None
        if title and author and price:
            try:
                payload = {
                    'title': title,
                    'author': author,
                    'price': float(price),
                    'description': description,
                    'stock': int(stock or 0),
                }
                if category_id:
                    payload['category_id'] = int(category_id)
                if publisher_id:
                    payload['publisher_id'] = int(publisher_id)

                r = requests.put(
                    f"{BOOK_SERVICE_URL}/api/books/{book_id}/",
                    json=payload,
                    timeout=5
                )
                if r.status_code == 200:
                    messages.success(request, 'Đã cập nhật sách thành công!')
                    return redirect('staff_book_list')
                try:
                    err = r.json()
                    msg = err.get('detail') or err
                except ValueError:
                    msg = r.text or f"Lỗi khi cập nhật (HTTP {r.status_code})."
                messages.error(request, msg)
            except requests.RequestException:
                messages.error(request, 'Không thể kết nối đến Book Service.')
        else:
            messages.error(request, 'Vui lòng điền đầy đủ thông tin.')

    book = None
    try:
        r = requests.get(f"{BOOK_SERVICE_URL}/api/books/{book_id}/", timeout=5)
        if r.status_code == 200:
            book = r.json()
    except requests.RequestException:
        messages.error(request, 'Không tìm thấy sách.')
        return redirect('staff_book_list')
    if not book:
        return redirect('staff_book_list')
    return render(request, 'staff_book_form.html', {
        'book': book,
        'action': 'edit',
        'categories': categories,
        'publishers': publishers,
    })


@csrf_protect
def staff_book_delete(request, book_id):
    """Staff: xóa sách."""
    if request.method == 'POST':
        try:
            r = requests.delete(f"{BOOK_SERVICE_URL}/api/books/{book_id}/", timeout=5)
            if r.status_code in (200, 204):
                messages.success(request, 'Đã xóa sách!')
            else:
                try:
                    err = r.json()
                    msg = err.get('detail') or err
                except ValueError:
                    msg = r.text or f"Không thể xóa sách (HTTP {r.status_code})."
                messages.error(request, msg)
        except requests.RequestException:
            messages.error(request, 'Không thể kết nối đến Book Service.')
    return redirect('staff_book_list')
