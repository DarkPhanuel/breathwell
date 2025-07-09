FROM python:3.11-slim

WORKDIR /app

# Environnement Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

# Installer les dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-traditional \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copier le projet
COPY . /app/

# Créer les dossiers nécessaires
RUN mkdir -p /app/models /app/staticfiles /app/media

# Copier et rendre l'entrée exécutable
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Point d’entrée du conteneur
ENTRYPOINT ["/app/entrypoint.sh"]
