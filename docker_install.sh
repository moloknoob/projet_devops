#!/bin/bash

# Mettre à jour les paquets existants
echo "Mise à jour des paquets..."
apt update -y
apt upgrade -y

# Installer les dépendances nécessaires pour Docker
echo "Installation des dépendances..."
apt install apt-transport-https ca-certificates curl software-properties-common -y

# Ajouter la clé GPG de Docker
echo "Ajout de la clé GPG de Docker..."
curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Ajouter le dépôt Docker pour Debian
echo "Ajout du dépôt Docker pour Debian..."
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Mettre à jour les sources de paquets
echo "Mise à jour des sources de paquets..."
apt update -y

# Installer Docker
echo "Installation de Docker..."
apt install docker-ce docker-ce-cli containerd.io -y

# Vérifier l'installation de Docker
echo "Vérification de l'installation de Docker..."
docker --version

# Activer Docker pour qu'il démarre automatiquement
echo "Activation du démarrage automatique de Docker..."
systemctl enable docker

# Démarrer Docker
echo "Démarrage de Docker..."
systemctl start docker

# Vérifier que Docker fonctionne bien
echo "Vérification que Docker fonctionne..."
docker run hello-world

# Vérifier que Kubernetes utilise Docker comme moteur de conteneur
echo "Vérification que Kubernetes utilise Docker..."

# Vérification du fichier de configuration Kubernetes kubelet
kubelet_config_file="/var/lib/kubelet/kubelet-config.yaml"
if [ -f "$kubelet_config_file" ]; then
  if grep -q "containerd" "$kubelet_config_file"; then
    echo "Kubernetes utilise containerd. Nous allons modifier la configuration pour utiliser Docker."
  
    # Modifier la configuration Kubernetes pour utiliser Docker
    sed -i 's/containerd/docker/' "$kubelet_config_file"
    echo "Configuration modifiée pour utiliser Docker."
    
    # Redémarrer kubelet pour appliquer les modifications
    systemctl restart kubelet
  else
    echo "Kubernetes utilise déjà Docker comme moteur de conteneur."
  fi
else
  echo "Le fichier de configuration kubelet n'a pas été trouvé. Assurez-vous que Kubernetes est installé correctement."
fi

echo "Installation de Docker terminée et Kubernetes configuré pour utiliser Docker !"
