# Benchmark d’outils JS pour les tests de charge

| Outil             | Langage   | Avantages                                 | Inconvénients                             |
|-------------------|-----------|-------------------------------------------|-------------------------------------------|
| k6                | JS / Go   | CLI performant, scripting flexible, CI/CD facile | Peu de visualisation intégrée par défaut |
| Artillery         | JS        | Syntaxe simple (YAML), facile à apprendre | Moins rapide pour de très gros tests     |
| Jest + Puppeteer  | JS        | Intègre UI + API dans un seul outil       | Peu adapté aux tests de charge massifs   |

## Liens utiles

- [k6 Documentation](https://k6.io/docs)
- [Artillery Documentation](https://www.artillery.io/docs)
- [Puppeteer GitHub](https://github.com/puppeteer/puppeteer)
- [Locust](https://locust.io/) (outil Python utilisé pour ce projet)
