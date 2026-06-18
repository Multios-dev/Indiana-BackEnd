# État actuel du projet — Indiana BackEnd

_Document généré le 2026-06-18, basé sur l'état du dépôt sur la branche `main`._

## 1. Vue d'ensemble

Indiana BackEnd est une API REST développée avec **FastAPI** (Python, async) destinée à gérer les données d'une organisation de type scoutisme : utilisateurs, organisations (unités, fédération, groupes externes...), mandats (memberships), événements, adresses et contacts.

La base de données est **PostgreSQL**, accédée en asynchrone via **SQLAlchemy 2.0** (`asyncpg`), avec les migrations gérées par **Alembic**.

## 2. Stack technique

| Composant | Technologie |
|---|---|
| Framework API | FastAPI ~0.135.1 |
| ORM | SQLAlchemy ~2.0.48 (async) |
| Driver DB | asyncpg ~0.31.0 (+ psycopg2-binary pour Alembic) |
| Migrations | Alembic ~1.18.4 |
| Validation | Pydantic (extra `email`) |
| Conteneurisation | `Dockerfile` présent mais **vide** |
| Workflow Git | git-flow (config dans `git-flow-plus.config`) — master: `main`, release: `dev`, test: `auth` |

## 3. Architecture du code

```
app/
├── api/routes/        # Endpoints FastAPI (users, organizations, memberships, events)
├── core/               # Config, exceptions métier, sécurité, gestion Redis des exceptions
├── db/
│   ├── models/         # Modèles SQLAlchemy (User, Organization, Membership, Event, Address, Contact)
│   ├── repositories/   # Pattern repository (interface + implémentation) par entité
│   ├── session.py      # Engine + sessionmaker async
│   ├── init_db.py      # Création des tables au démarrage si absentes
│   └── model_loader.py # Auto-import des modèles pour Alembic/SQLAlchemy
├── schemas/dtos/       # DTOs Pydantic input/output par entité
└── services/           # Logique métier (un service par entité)
alembic/versions/        # 29 migrations
tests/                   # Vide (seulement __init__.py, aucun test écrit)
```

Le projet suit une architecture en couches assez propre : **route → service → repository → modèle**, avec des exceptions métier centralisées (`app/core/exceptions.py`) traitées par un handler global (`app/core/redis/exception_handlers.py`).

## 4. Modèle de données

- **User** : personne physique. Prénoms stockés en JSON (multi-prénoms), nom, date de naissance, genre, totem, qualification scoute, statut représentant légal. Lien vers une adresse de domicile (obligatoire) et une adresse résidentielle (optionnelle).
- **Organization** : structure hiérarchique auto-référencée (parent/enfants), typée via l'enum `OrganizationType` (région, unité, section, patrouille, sizaine, association, instance fédérale, commission, partenaire externe, etc.).
- **Membership** : table de liaison User ↔ Organization avec rôle, dates de début/fin et prix (mandat).
- **Event** : événement hiérarchique (parent/enfants), géolocalisé (lat/long), relié en N-N à des **Audience** (table d'association `event_audience`).
- **Address** : adresse postale réutilisable (domicile/résidence).
- **Contact** : email/téléphone/site web, rattachable soit à un User soit à une Organization.

29 migrations Alembic ont été appliquées, montrant une évolution itérative du schéma (renommages de tables, ajout de cascades de suppression, corrections de modèles, ajout des adresses/mandats/événements).

## 5. API actuelle (CRUD complet sur 4 ressources)

| Ressource | Endpoints |
|---|---|
| `/users` | POST, GET (liste), GET /{id}, PUT /{id}, DELETE /{id} |
| `/organizations` | POST, GET (liste), GET /{id}, PUT /{id}, DELETE /{id} |
| `/memberships` | POST, GET (liste), GET /{id}, PUT /{id}, DELETE /{id} |
| `/events` | POST, GET (liste), GET /{id}, PUT /{id}, DELETE /{id} |

Chaque endpoint possède un `response_model` Pydantic dédié pour la validation automatique des réponses. Pas de pagination ni de filtres visibles sur les listes.

## 6. Points d'attention / dette technique

- **Sécurité — secret en clair** : `app/db/session.py` contient l'URL de connexion PostgreSQL **en dur dans le code**, avec identifiants et mot de passe visibles (hébergé chez OVH Cloud). À déplacer en variable d'environnement / secret manager au plus vite, surtout si ce dépôt est ou sera public.
- `app/core/config.py` et `app/core/security.py` existent mais sont **vides** — pas de gestion centralisée de la config, pas d'authentification/autorisation implémentée pour l'instant (branche `feature/auth` existe à part, non mergée).
- `Dockerfile` présent mais vide — la conteneurisation n'est pas encore opérationnelle.
- **Aucun test** : le dossier `tests/` ne contient qu'un `__init__.py` vide.
- `README.md` vide — pas de documentation d'installation/usage pour l'instant.
- Pas de fonctionnalité d'envoi de mails malgré la branche `feature/envoi-mails` existante côté remote.
- Présence d'un fichier `app.zip` (~108 Ko) à la racine du dépôt — à vérifier si volontaire (archive de build ?) avant de committer plus avant.
- Présence de fichiers `.pyc` compilés trackés dans git (`__pycache__/*.cpython-312.pyc`) — à ajouter au `.gitignore` si ce n'est pas déjà fait, pour éviter de polluer l'historique.

## 7. Branches actives (remote)

En plus de `main` et `dev`, de nombreuses branches `feature/*` existent côté remote, dont certaines semblent non mergées :
`feature/auth`, `feature/envoi-mails`, `feature/participation`, `feature/correction-bugs`, `feature/correction-suppression`, `feature/validations`, `feature/changement-db`, `feature/persons-api`, `feature/org-api`, `feature/mandat-api`, `feature/branche-test-feature`, `feature/address-user` (déjà mergée dans `dev` selon le dernier commit de merge).

## 8. Historique récent (derniers commits sur `main`)

```
c2fd127 gitflow test
b9d4e0f wq Merge branch 'feature/address-user' into dev
2ab6ae3 test
9ed8293 correction
7023e07 changement db
6e569c3 correction retour suppression événements
389c793 correction retour suppression mandats
86959bb correction retour suppression orga
22542cf correction retour suppression user
3329c2a corrections
7659fd4 validations pour les champs événements
218286f validations pour les champs mandats
de2a6c9 validations pour les champs organisations
74e5dcf validations pour les champs utilisateurs
```

Le projet est dans une phase de **stabilisation des CRUD de base** (validations de champs, gestion des suppressions en cascade) avant d'attaquer l'authentification et les fonctionnalités avancées.

## 9. Prochaines étapes suggérées

1. Sécuriser la connexion DB (variables d'environnement / `.env` + `app/core/config.py`).
2. Implémenter l'authentification (`feature/auth`) et remplir `app/core/security.py`.
3. Écrire des tests (le dossier `tests/` est prêt mais vide).
4. Finaliser le `Dockerfile` pour permettre un déploiement conteneurisé.
5. Nettoyer le dépôt : retirer `app.zip` et les `.pyc` du suivi git si non nécessaires.
6. Rédiger un `README.md` minimal (installation, lancement, variables d'env requises).
