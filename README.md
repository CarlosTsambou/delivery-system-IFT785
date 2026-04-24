# delivery-system-IFT785# Système de gestion de livraison de colis — IFT785

Système backend de suivi et d'optimisation de livraisons de colis développé avec FastAPI.
Il gère le cycle de vie complet d'un colis (créé → en transit → livré → confirmé),
envoie des notifications par email et offre un tableau de bord de statistiques.

## Prérequis

- Python 3.11+
- Git

## Installation

```bash
git clone https://github.com/CarlosTsambou/delivery-system-IFT785.git
cd delivery-system-IFT785
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Lancer le serveur

```bash
uvicorn app.main:app --reload
```

Accéder à la documentation interactive : http://127.0.0.1:8000/docs

## Lancer les tests

```bash
pytest tests/ -v --cov=app
```
## Modules implémentés

- M1 — Gestion des colis : CRUD complet, cycle de vie avec transitions validées
- M3 — Suivi temps réel : notifications email automatiques à chaque changement de statut
- M6 — Tableau de bord : statistiques globales, par statut et par période

## API externe

Notifications email via SMTP (Gmail / SendGrid).
Configuration dans le fichier `.env` :

EMAIL_EXPEDITEUR=votre@email.com
EMAIL_MOT_DE_PASSE=votre_mot_de_passe
SMTP_SERVEUR=smtp.gmail.com
SMTP_PORT=587

## Stack technique

- FastAPI + Uvicorn
- SQLAlchemy + SQLite
- Pydantic
- pytest + pytest-cov

## Design Patterns

Voir PATTERNS.md pour le détail des 8 patterns implémentés.
