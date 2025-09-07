# Usage: locust -f locustfile.py --headless --users 10 --spawn-rate 1 -H http://localhost:8000
from locust import HttpUser, between, task


class HT(HttpUser):
    wait_time = between(1, 5)

    @task(10)
    def default_page(self):
        self.client.get("/")
