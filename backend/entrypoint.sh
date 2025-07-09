#!/bin/bash

set -e  # Stop the script if any command fails

# Attente de la base de données PostgreSQL
if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."

    while ! nc -z "$DB_HOST" "$DB_PORT"; do
        echo "PostgreSQL not available yet..."
        sleep 1
    done

    echo "PostgreSQL is up!"
fi

# Appliquer les migrations
echo "Applying database migrations..."
python manage.py migrate

sleep 2

# Créer le superutilisateur si nécessaire (commande personnalisée)
echo "Creating superuser if none exists..."
python manage.py create_superuser_if_none_exists

# Collecte des fichiers statiques
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Démarrage du serveur
echo "Starting Django..."
exec "$@"
