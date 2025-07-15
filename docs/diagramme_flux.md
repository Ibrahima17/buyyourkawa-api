# Diagramme de flux – Fiabilité des données

```mermaid
flowchart TD
    A[Client Frontend] -->|Envoie requête| B[API FastAPI]
    B --> C{Validation Pydantic}
    C -->|Données valides| D[Contrôleur API]
    C -->|Données invalides| E[Erreur 422 Unprocessable Entity]

    D --> F[JWT : Vérification signature & expiration]
    F -->|Valide| G[Accès accordé]
    F -->|Invalide/expiré| H[401 Unauthorized]

    G --> I[Base de données (Simulée)]
    I --> J[Enregistrement OK]

    G --> K[Monitoring Prometheus]
    K --> L[Métriques exposées]

    J --> M[Logs RabbitMQ (si activé)]
