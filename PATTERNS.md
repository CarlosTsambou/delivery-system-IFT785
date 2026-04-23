Design Patterns — Système de gestion de livraison de colis

      Patterns GoF implémentés



1. Repository Pattern
Fichier :`app/repositories/colis_repository.py`  
Description :Isole la logique d'accès aux données de la logique métier. Toutes les requêtes SQLAlchemy passent par `ColisRepository` — les routes FastAPI ne connaissent pas la base de données directement.  
Principe SOLID associé :SRP — une seule responsabilité par classe.


2. Singleton Pattern
Fichier : `app/database.py`  
Description : `SessionLocal` est une fabrique de sessions unique configurée une seule fois. Une seule instance du moteur de base de données (`engine`) est créée pour toute l'application.  
Principe SOLID associé : DIP — les dépendances sont injectées via `get_db()`.


3. Observer Pattern
Fichier :`app/notifications/observer.py`, `app/notifications/email_notifier.py`  
Description :`SujetColis` maintient une liste d'observateurs (`ObservateurColis`). Quand un statut change, `notifier_tous()` est appelé automatiquement et chaque observateur réagit indépendamment. `NotificateurEmail` est un observateur concret.  
Principe SOLID associé : OCP — ajouter un nouveau type de notification (SMS, webhook) ne modifie pas le code existant.


4. State Pattern
Fichier :`app/services/colis_service.py`  
Description : Le cycle de vie d'un colis suit des transitions strictes : `créé → en_transit → livré → confirmé`. `TRANSITIONS_VALIDES` définit les états autorisés. Toute transition invalide retourne une erreur `400` avec un message explicite.  
**Principe SOLID associé :** OCP — ajouter un nouvel état ne nécessite que d'étendre le dictionnaire.


5. Template Method Pattern
Fichier :`app/notifications/observer.py`  
Description :`ObservateurColis` est une classe abstraite qui définit le squelette de la notification via la méthode abstraite `notifier()`. Chaque sous-classe implémente son propre comportement concret.  
Principe SOLID associé :LSP — toute sous-classe d'`ObservateurColis` peut remplacer la classe abstraite sans changer le comportement du système.


6. Strategy Pattern
Fichier : `app/services/dashboard_service.py`  
Description :`DashboardService` délègue le calcul des statistiques à une stratégie interchangeable (`StrategieStatistique`). Trois stratégies concrètes : `StatistiqueGlobale`, `StatistiqueParStatut`, `StatistiqueParPeriode`. On change d'algorithme à la volée via `definir_strategie()`.  
Principe SOLID associé :OCP — ajouter une nouvelle statistique = créer une nouvelle classe sans modifier `DashboardService`.


7. Factory Pattern
Fichier :`app/repositories/colis_repository.py`  
Description :La méthode `creer()` de `ColisRepository` encapsule la création d'un objet `Colis`. Le code appelant ne connaît pas les détails de construction (UUID, dates, statut initial) — il reçoit simplement un colis prêt à l'emploi.  
Principe SOLID associé :SRP — la création est isolée dans une méthode dédiée.


8. Dependency Injection Pattern
Fichier :`app/routers/colis.py`, `app/routers/dashboard.py`  
Description : FastAPI injecte automatiquement la session de base de données dans chaque route via `Depends(get_db)`. Aucune route ne crée sa propre connexion — elles reçoivent leur dépendance de l'extérieur.  
Principe SOLID associé :DIP — les modules de haut niveau (routes) ne dépendent pas des modules de bas niveau (BD), ils dépendent d'une abstraction (`get_db`).


Principes SOLID démontrés


SRP `ColisRepository`, `ColisService` : Chaque classe a une seule responsabilité
OCP `ObservateurColis`, `StrategieStatistique`: Extensible sans modification 
LSP `NotificateurEmail`  Remplace `ObservateurColis` sans changer le système 
ISP `StrategieStatistique`  Interface minimale, une seule méthode 
DIP `Depends(get_db)`  Injection de dépendances FastAPI 

API externe intégrée

SendGrid / SMTP — `app/notifications/email_notifier.py`  
Envoi d'email automatique à chaque changement de statut d'un colis. En mode développement, la notification est simulée dans les logs.