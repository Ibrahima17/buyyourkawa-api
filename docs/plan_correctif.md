# 🛠️ Plan d’actions correctives – Exemple

| Endpoint   | KPI Observé | Seuil    | Problème                  | Action Corrective                    | Délai |
|------------|--------------|----------|---------------------------|--------------------------------------|-------|
| `/token`   | 980 ms       | < 300 ms | Temps de réponse trop long| Mise en cache Redis                  | 48h   |
| `/client`  | 5% erreurs   | < 1 %    | Trop d’erreurs 500        | Validation stricte des entrées       | 72h   |
| `/metrics` | Non dispo    | Toujours | Monitoring indisponible   | Revoir exposition Prometheus         | 24h   |
