from locust import HttpUser, task, between

class BuyYourKawaUser(HttpUser):
    wait_time = between(1, 3)  # Temps d'attente entre chaque requête

    @task
    def read_root(self):
        self.client.get("/")

    @task
    def get_token(self):
        self.client.post("/token", data={
            "username": "user",
            "password": "password"
        })
