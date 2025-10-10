# Flaty

Flaty est une application web qui agrège les annonces immobilières de plusieurs sites (SeLoger, PAP, Bien'ici) pour faciliter la recherche de location.

## Installation

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows
.\venv\Scripts\activate
# Sur Unix
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

## Utilisation

```bash
python flaty.py
```

L'application sera accessible à l'adresse : http://localhost:8050

## Structure du projet

```
flaty/
├── assets/           # Ressources statiques (images, css, etc.)
├── components/       # Composants réutilisables
│   ├── SearchInputs/    # Composants pour la recherche
│   └── SitesManager/    # Gestion des sites d'annonces
├── pages/           # Pages de l'application
├── src/            # Code source principal
│   ├── build_url.py     # Construction des URLs
│   └── constants.py     # Constantes
├── tests/          # Tests unitaires
├── flaty.py        # Point d'entrée de l'application
└── requirements.txt # Dépendances du projet
```

## Contribution

1. Fork le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## License

[MIT](https://choosealicense.com/licenses/mit/)