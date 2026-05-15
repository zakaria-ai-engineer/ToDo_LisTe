# ── Backend Dockerfile ─────────────────────────────────────────────────────
# Image de base : Python 3.11 slim pour minimiser la taille
FROM python:3.11-slim

# Métadonnées
LABEL maintainer="TaskBot AI"

# Dossier de travail
WORKDIR /app

# 1. Copier requirements en premier (optimisation des couches Docker)
#    -> Si requirements.txt ne change pas, cette couche est mise en cache
COPY requirements.txt .

# 2. Installer les dépendances Python (sans cache pip pour réduire la taille)
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copier tout le code source
COPY . .

# Port exposé
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
