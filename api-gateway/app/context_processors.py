import os
import requests

CUSTOMER_SERVICE_URL = os.getenv("CUSTOMER_SERVICE_URL", "http://localhost:8001")


def current_customer(request):
    """Đưa thông tin khách hàng đang chọn (từ session) vào mọi template."""
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return {"current_customer": None}

    try:
        resp = requests.get(
            f"{CUSTOMER_SERVICE_URL}/api/customers/{customer_id}/",
            timeout=3
        )
        if resp.status_code == 200:
            return {"current_customer": resp.json()}
    except requests.RequestException:
        pass
    return {"current_customer": None}
