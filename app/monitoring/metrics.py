
from prometheus_client import Counter, Histogram, make_asgi_app

# QPS
REQUEST_COUNT = Counter("chat_requests_total", "Total number of /chat requests")

# Latency
REQUEST_LATENCY = Histogram(
    "chat_request_latency_seconds",
    "Latency of /chat endpoint in seconds",
    buckets=(0.05, 0.1, 0.2, 0.5, 1, 2, 5),
)

# 將 Prometheus WSGI app 轉為 ASGI app，給 FastAPI mount
metrics_app = make_asgi_app()
