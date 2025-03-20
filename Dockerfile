FROM python:3.7-alpine

# Définir le répertoire de travail
WORKDIR /app

# Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
COPY . .

# Définir la variable d'environnement pour Flask
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

# Exécuter Flask avec python directement pour éviter les erreurs d'import
CMD ["python", "-m", "flask", "run"]

#CMD ["python", "run.py"]