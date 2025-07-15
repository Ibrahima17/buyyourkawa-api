# Diagramme de flux – Fiabilité des données

```mermaid
flowchart TD
    Front[Client Frontend] -->|Envoie requête| API[API FastAPI]
    API --> Validate{Validation Pydantic}
    Validate -->|Valide| Controller[Contrôleur API]
    Validate -->|Invalide| Error422[Erreur 422 Unprocessable Entity]

    Controller --> JWT[JWT Vérification]
    JWT -->|Valide| Access[Accès accordé]
    JWT -->|Expiré/Invalide| Error401[401 Unauthorized]

    Access --> DB[Base de données Simulée]
    DB --> Save[Enregistrement OK]

    Access --> Metrics[Monitoring Prometheus]
    Metrics --> Exposed[Métriques exposées]

    Save --> Queue[RabbitMQ Logs]
