# Système de Test de Localisation WiFi vs 4G

## Description du projet
Ce dépôt contient un système de test développé pour comparer les performances des technologies de localisation WiFi et 4G. Ce système peut être utilisé pour évaluer la précision, la fiabilité et la stabilité de différentes sources de géolocalisation dans divers environnements.

## Objectifs
- Comparer la précision des technologies de localisation basées sur le WiFi et la 4G
- Fournir des données empiriques sur les performances de ces technologies
- Offrir un outil open source pour tester la géolocalisation dans différents contextes

## Fonctionnalités

### Suivi de localisation
- Démarrer/arrêter le suivi de localisation
- Basculer entre connexion 4G et WiFi
- Configurer l'intervalle de mise à jour de la localisation

### Visualisation des données
- Affichage des données de localisation sur une carte
- Filtrage des données par période (dernière heure, dernier jour, etc.)
- Statistiques sur la précision et la vitesse

### Gestion des données
- Suppression des données enregistrées
- Export des données au format CSV pour analyse externe

## Architecture technique

### Technologies utilisées
- **Frontend** : HTML et JavaScript avec l'API de géolocalisation
- **Backend** : Flask (Python) pour le traitement et le stockage des données
- **Base de données** : MongoDB pour la persistance des données de localisation

### Implémentation de l'API de Géolocalisation
Le système utilise l'API Geolocation du navigateur avec les méthodes suivantes :
```javascript
// Exemple d'implémentation
async function sendLocation() {
    try {
        const position = await new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(resolve, reject, {
                enableHighAccuracy: true,
                timeout: 5000,
                maximumAge: 0
            });
        });
        // Traitement des données de position
    } catch (error) {
        // Gestion des erreurs
    }
}
```

## Installation et utilisation

### Prérequis
- Python 3.7+
- MongoDB
- Navigateur web moderne supportant l'API Geolocation

### Installation
1. Cloner le dépôt
```bash
git clone https://github.com/votre-utilisateur/location-testing-system.git
cd location-testing-system
```

2. Installer les dépendances
```bash
pip install -r requirements.txt
```

3. Configurer la base de données MongoDB

4. Lancer l'application
```bash
python app.py
```

5. Accéder à l'application web via l'URL locale ou exposer via ngrok pour les tests mobiles

## Exemples de résultats

Lors de nos tests, nous avons observé les résultats suivants :

### WiFi
- Précision moyenne : 13,8 mètres
- Stabilité : Très bonne, mesures homogènes

### 4G
- Précision moyenne : 32,88 mètres
- Écart-type : 6,7 mètres
- Stabilité : Variable, fluctuations importantes

## Limitations connues
- L'API Geolocation ne précise pas directement la source de localisation (WiFi, 4G, GPS)
- Les performances peuvent varier selon le navigateur et le dispositif utilisés

## Contributions
Les contributions à ce projet sont les bienvenues. N'hésitez pas à ouvrir une issue ou à soumettre une pull request.
