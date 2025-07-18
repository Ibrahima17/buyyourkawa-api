from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    @task(2)
    def home(self):
        self.client.get("/")

    @task(1)
    def health(self):
        self.client.get("/healthcheck")

    @task(1)
    def info(self):
        self.client.get("/info")

    @task(2)
    def get_token(self):
        self.client.post("/token", data={"username": "user", "password": "password"})

    @task(1)
    def echo_post(self):
        self.client.post("/echo", json={"text": "Hello test"})
