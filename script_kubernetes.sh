#!/bin/bash

set -e  # Arrête le script en cas d'erreur

echo "🚀 Mise à jour des paquets..."
sudo apt-get update && sudo apt-get upgrade -y

echo "📥 Installation des dépendances..."
sudo apt-get install -y apt-transport-https ca-certificates curl gpg software-properties-common

echo "🔑 Ajout de la clé GPG de Kubernetes..."
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

echo "📌 Ajout du dépôt Kubernetes..."
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list

echo "🔄 Mise à jour des dépôts..."
sudo apt-get update

echo "📦 Installation de kubelet, kubeadm et kubectl..."
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl  # Empêche la mise à jour accidentelle

echo "✅ Installation réussie ! 🚀"
echo "➡️ Lance 'kubeadm init' pour initialiser le cluster Kubernetes."
