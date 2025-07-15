# Qualité des Données - BuyYourKawa API

| Champ          | Type    | Contraintes                                      | Norme         |
|----------------|---------|--------------------------------------------------|---------------|
| user_email     | string  | non null, regex format email RFC 5322            | RFC 5322      |
| created_at     | date    | non null                                         | ISO 8601      |
| access_token   | string  | JWT signé, expiré après 30 min                   | RFC 7519 JWT  |
| client_id      | UUID    | unique, non null                                 | RFC 4122      |
| address        | string  | max length 255, non null                         | UTF-8         |
| logs           | object  | contient method, endpoint, status, latency       | JSON, Prometheus exposition |
