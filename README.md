# Delivery System — IFT785

[![Language: Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://www.python.org/)
[![Framework: FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Database: SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg)](https://www.sqlite.org/)
[![Tests: pytest](https://img.shields.io/badge/Tests-pytest-0A9EDC.svg)](https://pytest.org/)

> Système de gestion de livraisons avec API REST — projet académique IFT785 · Université de Sherbrooke · Hiver 2026

---

## Aperçu

Application backend complète pour la gestion d'un système de livraisons. Le projet met en œuvre une architecture modulaire orientée maintenabilité avec séparation claire des couches (domaine / application / infrastructure).

---

## Fonctionnalités

- API REST complète (CRUD) pour la gestion des commandes et livraisons
- Architecture modulaire — séparation domaine / application / infrastructure
- Persistance des données avec SQLite
- Tests automatisés avec pytest et mesure de couverture
- Validation des données et gestion des erreurs

---

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| Backend | Python · FastAPI |
| Base de données | SQLite |
| Tests | pytest · coverage |
| Qualité | flake8 · revue de code |

---

## Structure du projet

```
delivery-system-IFT785/
├── app/
│   ├── domain/          # Entités métier et règles de gestion
│   ├── application/     # Services et cas d'utilisation
│   └── infrastructure/  # Accès base de données, routes API
├── tests/               # Tests unitaires et d'intégration
├── requirements.txt
└── README.md
```

---

## Installation et exécution

```bash
# Cloner le repo
git clone https://github.com/CarlosTsambou/delivery-system-IFT785.git
cd delivery-system-IFT785

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
uvicorn app.main:app --reload

# Lancer les tests
pytest tests/ -v --cov=app
```

L'API est accessible à `http://localhost:8000` — documentation interactive disponible sur `/docs`.

---

## Auteur

**Carlos Tsambou Jiofack**  
[github.com/CarlosTsambou](https://github.com/CarlosTsambou) · [linkedin.com/in/carlos-tsambou-jiofack](https://linkedin.com/in/carlos-tsambou-jiofack)
