from fastapi import FastAPI, Request, HTTPException, Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from pydantic import BaseModel
from models import Client, Address
from typing import List
from datetime import datetime, timedelta, timezone
import uuid
import jwt
import pika

# Clé secrète et algorithme pour signer les JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# Initialisation de l'application FastAPI
app = FastAPI(
    title="BuyYourKawa API",
    description="API pour la gestion des clients de l'application BuyYourKawa",
    version="1.0.0",
    contact={
        "name": "Support BuyYourKawa",
        "email": "support@buyyourkawa.com",
    },
)

# Configuration OAuth2 pour l'authentification
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Métriques Prometheus pour le monitoring
REQUEST_COUNT = Counter('request_count', 'Total number of requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency', ['method', 'endpoint'])
REQUEST_SUCCESS = Counter('request_success', 'Number of successful requests', ['method', 'endpoint'])
REQUEST_FAILURE = Counter('request_failure', 'Number of failed requests', ['method', 'endpoint'])

# Base de données simulée pour les clients et les utilisateurs
clients_db = []
users_db = {
    "user": {
        "username": "user",
        "password": "password"
    }
}


# Modèle Pydantic pour les messages
class Message(BaseModel):
    message: str


# Middleware pour mesurer le temps de traitement des requêtes
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    method = request.method
    endpoint = request.url.path
    REQUEST_COUNT.labels(method, endpoint).inc()
    with REQUEST_LATENCY.labels(method, endpoint).time():
        response = await call_next(request)
        if 200 <= response.status_code < 300:
            REQUEST_SUCCESS.labels(method, endpoint).inc()
        else:
            REQUEST_FAILURE.labels(method, endpoint).inc()
    return response


# Fonction pour authentifier un utilisateur
def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if not user or user["password"] != password:
        return False
    return user


# Fonction pour créer un jeton d'accès (JWT)
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Endpoint pour obtenir un jeton d'accès
@app.post("/token", summary="Obtenir un jeton d'accès", description="Génère un jeton JWT pour l'authentification")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


# Fonction pour obtenir l'utilisateur actuel à partir du jeton JWT
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Jeton invalide")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Jeton expiré")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Jeton invalide")


# Fonction pour envoyer un message à RabbitMQ
def send_message_to_rabbitmq(queue: str, message: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange='', routing_key=queue, body=message)
    connection.close()
    print(f" [x] Sent '{message}'")


# Endpoint pour envoyer un message
@app.post("/send")
def send_message(message: Message, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_message_to_rabbitmq, 'hello', message.message)
    return {"message": "Message sent to RabbitMQ"}


# Fonction callback pour recevoir les messages de RabbitMQ
def callback(ch, method, properties, body):
    print(f" [x] Received {body}")


# Fonction pour recevoir des messages de RabbitMQ
def receive_messages_from_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


# Endpoint pour démarrer la réception des messages
@app.get("/receive")
def receive_messages(background_tasks: BackgroundTasks):
    background_tasks.add_task(receive_messages_from_rabbitmq)
    return {"message": "Started receiving messages from RabbitMQ"}


# Endpoint pour créer un nouveau client
@app.post("/clients", response_model=Client, summary="Créer un nouveau client",
          description="Crée un nouveau client dans la base de données.")
async def create_client(client: Client, background_tasks: BackgroundTasks, token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token)
    client.id = str(uuid.uuid4())
    client.created_at = datetime.now(timezone.utc)
    client.updated_at = datetime.now(timezone.utc)
    clients_db.append(client)

    background_tasks.add_task(send_message_to_rabbitmq, 'hello', f"Client créé : {client.name}")

    return client


# Endpoint pour obtenir tous les clients
@app.get("/clients", response_model=List[Client], summary="Obtenir tous les clients",
         description="Récupère tous les clients de la base de données.")
def get_clients(token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token)
    return clients_db


# Endpoint pour obtenir un client spécifique par ID
@app.get("/clients/{client_id}", response_model=Client, summary="Obtenir un client par ID",
         description="Récupère un client spécifique par ID.")
def get_client(client_id: str, token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token)
    client = next((c for c in clients_db if c.id == client_id), None)
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return client


# Endpoint pour mettre à jour un client spécifique
@app.put("/clients/{client_id}", response_model=Client, summary="Mettre à jour un client",
         description="Met à jour les détails d'un client spécifique.")
def update_client(client_id: str, client: Client, token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token)
    stored_client = next((c for c in clients_db if c.id == client_id), None)
    if not stored_client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    stored_client.name = client.name
    stored_client.email = client.email
    stored_client.phone = client.phone
    stored_client.address = client.address
    stored_client.updated_at = datetime.now(timezone.utc)
    return stored_client


# Endpoint pour supprimer un client spécifique
@app.delete("/clients/{client_id}", summary="Supprimer un client",
            description="Supprime un client spécifique de la base de données.")
def delete_client(client_id: str, token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token)
    global clients_db
    clients_db = [c for c in clients_db if c.id != client_id]
    return {"message": "Client supprimé avec succès"}


# Endpoint pour obtenir les métriques Prometheus pour le monitoring
@app.get("/metrics", summary="Obtenir les métriques Prometheus",
         description="Expose les métriques Prometheus pour le monitoring.")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
