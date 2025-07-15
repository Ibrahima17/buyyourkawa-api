# BuyYourKawa API – Projet FastAPI

Ce projet est une **API** développée avec **FastAPI**, pour gérer les clients de l’application *BuyYourKawa*.  
Il intègre l’authentification JWT, la validation des données, le monitoring Prometheus et un test de charge Locust.

---

## Fonctionnalités

-  Authentification OAuth2 avec JWT signé.
-  Validation des données via **Pydantic**.
-  Monitoring des requêtes avec **Prometheus**.
-  Traitements asynchrones (RabbitMQ prévu).
-  Tests de charge automatisés avec **Locust**.

---

---

##  Livrables du TP

### 1 **Qualité des données**

-  `docs/data_quality.md` : tableau des types de données manipulées, formats et contraintes.

### 2 **Fiabilité des données**

-  `docs/diagramme_flux.md` : diagramme de flux de la circulation des données.
-  `docs/plan_validations.md` : tableau des méthodes de validation.
-  `main.py` : code source avec validation Pydantic et JWT.

### 3 **Estimation de la charge utilisateur**

-  `load_test/locust_config.json` : hypothèses de charge.
- Scénario Locust prêt dans `locustfile.py`.

### 4 **Plan d’actions correctives**

-  `docs/plan_correctif.md` : tableau des actions à prendre après les tests.

### 5 **Benchmark d’outils JS (optionnel)**

-  `docs/benchmark_js.md` : comparaison K6 / Artillery / Puppeteer.

### 6 **Résultats tests Locust**

- `load_test/locust_results.png` : captures d’écran des graphiques et stats.
- Rapport CSV disponible si besoin.

### 7️⃣ **Code source sur GitHub**

---

##  Lancer le projet

```bash
# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer FastAPI
uvicorn main:app --reload

# Navigateur
Mettez vous sur http://127.0.0.1:8000/docs ou http://127.0.0.1:8000/Redoc

# Lancer Locust
locust -f load_test/locustfile.py
