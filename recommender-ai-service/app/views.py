import os
import requests
from rest_framework.response import Response
from rest_framework.views import APIView

BOOK_SERVICE_URL = os.getenv("BOOK_SERVICE_URL", "http://localhost:8003")
COMMENT_RATE_SERVICE_URL = os.getenv("COMMENT_RATE_SERVICE_URL", "http://localhost:8010")


class RecommendView(APIView):
    """
    Gợi ý sách đơn giản:
    - Lấy rating trung bình từ comment-rate-service
    - Sắp xếp theo điểm cao nhất
    """

    def get(self, request, customer_id=None):
        try:
            ratings_resp = requests.get(
                f"{COMMENT_RATE_SERVICE_URL}/api/ratings/",
                timeout=5
            )
            books_resp = requests.get(
                f"{BOOK_SERVICE_URL}/api/books/",
                timeout=5
            )
        except requests.RequestException:
            return Response({"detail": "Không kết nối được tới services."}, status=503)

        if ratings_resp.status_code != 200 or books_resp.status_code != 200:
            return Response({"detail": "Lỗi khi lấy dữ liệu nguồn."}, status=502)

        ratings = ratings_resp.json()
        books = {b["id"]: b for b in books_resp.json()}

        # tính rating trung bình theo book_id
        stats = {}
        for r in ratings:
            bid = r.get("book_id")
            if bid not in books:
                continue
            stats.setdefault(bid, {"sum": 0, "count": 0})
            stats[bid]["sum"] += r.get("rating", 0)
            stats[bid]["count"] += 1

        scored = []
        for bid, s in stats.items():
            avg = s["sum"] / s["count"]
            scored.append({
                "book_id": bid,
                "title": books[bid]["title"],
                "score": avg,
            })

        scored.sort(key=lambda x: x["score"], reverse=True)
        top_n = int(request.query_params.get("limit", 5))
        return Response(scored[:top_n])