# SmartCity Lyon - Docker Frontend

Configuration Docker simple pour le frontend uniquement de l'application SmartCity Lyon.

## 🚀 Utilisation

### Construction de l'image

```bash
docker build -t smartcity-lyon-frontend .
```

### Lancement du conteneur

```bash
docker run -d \
  --name smartcity-lyon \
  -p 3000:80 \
  smartcity-lyon-frontend
```

### Accès à l'application

- **Web**: http://localhost:3000

## 🔧 Configuration

### Variables d'environnement

Vous pouvez passer des variables d'environnement au moment du build :

```bash
docker build \
  --build-arg VITE_API_URL=http://votre-backend.com/api \
  -t smartcity-lyon-frontend .
```

### Proxy API

Le fichier `nginx.conf` inclut une configuration de proxy pour rediriger les appels `/api/` vers votre serveur backend. 

Par défaut, il pointe vers `http://host.docker.internal:8000/`. Modifiez cette URL dans `nginx.conf` selon votre configuration backend.

## 🛠️ Commandes utiles

```bash
# Voir les logs du conteneur
docker logs smartcity-lyon

# Arrêter le conteneur
docker stop smartcity-lyon

# Supprimer le conteneur
docker rm smartcity-lyon

# Supprimer l'image
docker rmi smartcity-lyon-frontend
```

## 📋 Structure

- **Dockerfile** : Configuration multi-stage (build + production)
- **nginx.conf** : Configuration Nginx avec proxy API
- **.dockerignore** : Fichiers exclus du contexte Docker

## 🔒 Sécurité

L'image inclut :
- Headers de sécurité HTTP
- Compression gzip
- Cache optimisé pour les assets statiques
- Health check intégré
- Déni d'accès aux fichiers sensibles

## 🏥 Health Check

Un endpoint `/health` est disponible pour vérifier l'état du conteneur :

```bash
curl http://localhost:3000/health
```