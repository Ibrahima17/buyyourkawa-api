# ✅ Plan de validations – Fiabilité des données

| Vérification                  | Niveau     | Méthode                     | Outil / Librairie         |
|-------------------------------|------------|-----------------------------|---------------------------|
| Format e-mail                 | Backend    | Regex + Pydantic            | `EmailStr` de Pydantic    |
| UUID client                   | Backend    | Vérification format UUID    | Pydantic `uuid.UUID`      |
| Champs obligatoires           | Backend    | Champs `required` Pydantic  | Modèles Pydantic          |
| Signature et expiration JWT   | Backend    | Décodage + vérification `exp` | `pyjwt`                   |
| Contraintes de doublons       | Backend    | Vérification clé unique     | Simulé : liste Python     |
| Cohérence des logs Prometheus | Backend    | Middleware de monitoring    | `prometheus_client`       |
| Sécurité des flux             | Backend    | HTTPS, OAuth2, JWT signé    | FastAPI Security + SSL    |
| Tests automatiques            | Backend    | Vérification requêtes API   | `pytest`, `httpx`         |
| Validation côté Front (bonus) | Frontend   | Champs obligatoires, Regex  | Formulaire JS / HTML5     |
